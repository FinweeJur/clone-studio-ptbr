import os
import uuid
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.config import settings
from app.services.subtitle_generator import SubtitleGenerator, SubtitleStyle
from app.services.audio_mixer import AudioMixer
from app.services.broll_manager import BrollManager
from app.services.remote_worker_client import RemoteWorkerClient

router = APIRouter()

class TestWorkerRequest(BaseModel):
    worker_url: str
    token: Optional[str] = None

class RenderProjectRequest(BaseModel):
    clone_id: str
    script_text: str
    subtitle_style: Optional[str] = SubtitleStyle.HORMOZI
    aspect_ratio: Optional[str] = "9:16"  # "9:16", "16:9", "1:1"
    bgm_asset_path: Optional[str] = None
    bgm_volume: Optional[float] = 0.15
    visual_layers: Optional[List[Dict[str, Any]]] = []
    render_mode: Optional[str] = "hybrid_worker"  # "hybrid_worker", "export_zip", "local_direct"
    worker_url: Optional[str] = None
    worker_token: Optional[str] = None

# Memória de jobs em andamento
JOBS_STORE: Dict[str, Dict[str, Any]] = {}

@router.post("/test-worker")
async def test_worker(req: TestWorkerRequest):
    """Testa se o Cloudflare Tunnel / Servidor Próprio está conectado e respondendo."""
    result = await RemoteWorkerClient.test_connection(req.worker_url, req.token)
    return result

@router.post("/export-package")
async def export_package(req: RenderProjectRequest):
    """Gera um arquivo .zip autônomo com os dados e script de renderização offline."""
    project_id = str(uuid.uuid4())[:8]
    zip_filename = f"CloneStudio_Export_{project_id}.zip"
    zip_path = settings.EXPORTS_DIR / zip_filename

    # Buscar perfil de clone
    profiles_db = settings.CLONES_DIR / "profiles.json"
    profiles = []
    if profiles_db.exists():
        with open(profiles_db, "r", encoding="utf-8") as f:
            profiles = json.load(f)
    
    clone = next((p for p in profiles if p["id"] == req.clone_id), None)
    if not clone or not clone.get("video_path"):
        raise HTTPException(status_code=400, detail="Perfil de clone não encontrado ou sem vídeo de referência.")

    avatar_video_path = Path(clone["video_path"])
    voice_sample_path = Path(clone["voice_sample_path"]) if clone.get("voice_sample_path") else None

    exported_zip = RemoteWorkerClient.create_export_package(
        project_id=project_id,
        script_text=req.script_text,
        avatar_video_path=avatar_video_path,
        voice_sample_path=voice_sample_path if voice_sample_path and voice_sample_path.exists() else None,
        timeline_cues=req.visual_layers or [],
        subtitle_style=req.subtitle_style or SubtitleStyle.HORMOZI,
        output_zip_path=zip_path
    )

    return {
        "status": "success",
        "project_id": project_id,
        "zip_url": f"/api/render/download-export/{zip_filename}",
        "message": "Pacote ZIP autônomo gerado com sucesso para processar em servidor externo ou Google Colab!"
    }

@router.get("/download-export/{filename}")
async def download_export(filename: str):
    """Faz download do arquivo .zip exportado."""
    file_path = settings.EXPORTS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(path=str(file_path), filename=filename, media_type="application/zip")

@router.post("/start-render")
async def start_render(req: RenderProjectRequest, background_tasks: BackgroundTasks):
    """Inicia o processo completo de renderização do vídeo."""
    job_id = str(uuid.uuid4())[:8]
    
    JOBS_STORE[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 5,
        "message": "Tarefa adicionada na fila de processamento...",
        "output_video": None
    }

    background_tasks.add_task(process_render_pipeline, job_id, req)
    return {"status": "success", "job_id": job_id}

@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Consulta o progresso e status de um trabalho de renderização."""
    if job_id not in JOBS_STORE:
        raise HTTPException(status_code=404, detail="Trabalho não encontrado")
    return JOBS_STORE[job_id]

@router.get("/download-video/{job_id}")
async def download_video(job_id: str):
    """Faz download do vídeo final MP4 gerado."""
    job = JOBS_STORE.get(job_id)
    if not job or not job.get("output_video"):
        raise HTTPException(status_code=404, detail="Vídeo ainda não pronto ou job inexistente.")
    
    video_path = Path(job["output_video"])
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo de vídeo não encontrado no disco.")
    
    return FileResponse(path=str(video_path), filename=f"clone_video_{job_id}.mp4", media_type="video/mp4")

async def process_render_pipeline(job_id: str, req: RenderProjectRequest):
    """Pipeline assíncrono de geração de áudio, talking head, B-Roll e legendas."""
    try:
        JOBS_STORE[job_id]["status"] = "processing"
        JOBS_STORE[job_id]["progress"] = 15
        JOBS_STORE[job_id]["message"] = "Carregando perfil e gerando fala em PT-BR..."

        # 1. Carregar perfil de clone
        profiles_db = settings.CLONES_DIR / "profiles.json"
        profiles = []
        if profiles_db.exists():
            with open(profiles_db, "r", encoding="utf-8") as f:
                profiles = json.load(f)
        clone = next((p for p in profiles if p["id"] == req.clone_id), None)
        
        avatar_ref_path = Path(clone["video_path"]) if clone and clone.get("video_path") else None
        
        job_dir = settings.OUTPUTS_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        speech_audio_path = job_dir / "speech.wav"
        
        # 2. Síntese de Voz (TTS / Clonagem)
        # Se temos worker remoto com GPU, ou se geramos síntese local
        JOBS_STORE[job_id]["progress"] = 35
        JOBS_STORE[job_id]["message"] = "Sintetizando voz e sincronizando movimentos faciais..."
        
        raw_avatar_video_path = job_dir / "raw_talking_head.mp4"
        
        # Modo A: Worker Remoto (Cloudflare / Servidor)
        if req.worker_url and req.render_mode == "hybrid_worker":
            video_bytes = await RemoteWorkerClient.dispatch_render_job(
                worker_url=req.worker_url,
                avatar_video_path=avatar_ref_path,
                audio_path=speech_audio_path,
                token=req.worker_token
            )
            with open(raw_avatar_video_path, "wb") as f:
                f.write(video_bytes)
        else:
            # Modo B: Renderizador Local / Fallback Leve
            # Se não houver worker remoto, cria o áudio via gTTS/Piper ou FFmpeg e sincroniza com o vídeo base
            if not speech_audio_path.exists():
                # Gera tom de áudio placeholder sincronizado com a duração aproximada do roteiro
                words_count = len(req.script_text.split())
                approx_duration = max(3.0, (words_count / 140.0) * 60.0)
                cmd_audio = [
                    "ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=frequency=440:duration={approx_duration}",
                    "-c:a", "pcm_s16le", str(speech_audio_path)
                ]
                subprocess.run(cmd_audio, check=True)

            # Loop do vídeo base para a duração da fala
            cmd_loop = [
                "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(avatar_ref_path),
                "-i", str(speech_audio_path), "-c:v", "libx264", "-c:a", "copy",
                "-shortest", str(raw_avatar_video_path)
            ]
            subprocess.run(cmd_loop, check=True)

        # 3. Mixagem de Áudio com BGM e Auto-Ducking
        JOBS_STORE[job_id]["progress"] = 60
        JOBS_STORE[job_id]["message"] = "Mixando trilha sonora com auto-ducking..."
        
        mixed_audio_path = job_dir / "mixed_audio.wav"
        if req.bgm_asset_path and Path(req.bgm_asset_path).exists():
            AudioMixer.mix_speech_with_bgm(
                speech_audio_path=speech_audio_path,
                bgm_audio_path=Path(req.bgm_asset_path),
                output_audio_path=mixed_audio_path,
                bgm_base_volume=req.bgm_volume or 0.15
            )
        else:
            mixed_audio_path = speech_audio_path

        # 4. Geração de Legendas Inteligentes
        JOBS_STORE[job_id]["progress"] = 75
        JOBS_STORE[job_id]["message"] = "Criando legendas estilizadas sem quebra de palavras..."
        
        # Segmentação simples ou baseada em frases para legendas
        sentences = [s.strip() for s in req.script_text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        segments = []
        seg_start = 0.0
        time_per_word = 0.4
        
        for sent in sentences:
            dur = max(1.5, len(sent.split()) * time_per_word)
            segments.append({
                "start": seg_start,
                "end": seg_start + dur,
                "text": sent
            })
            seg_start += dur

        sub_path = job_dir / "subtitles.ass"
        SubtitleGenerator.generate_ass_file(
            segments=segments,
            output_path=sub_path,
            style_name=req.subtitle_style or SubtitleStyle.HORMOZI
        )

        # 5. Composição de Camadas (B-Roll, Overlays e Montagem Final)
        JOBS_STORE[job_id]["progress"] = 90
        JOBS_STORE[job_id]["message"] = "Finalizando renderização e aplicando camadas de B-Roll..."
        
        final_video_path = job_dir / f"final_output_{job_id}.mp4"
        BrollManager.composite_video_layers(
            base_video_path=raw_avatar_video_path,
            audio_path=mixed_audio_path,
            subtitle_path=sub_path,
            visual_layers=req.visual_layers or [],
            output_video_path=final_video_path,
            aspect_ratio=req.aspect_ratio or "9:16"
        )

        JOBS_STORE[job_id]["status"] = "completed"
        JOBS_STORE[job_id]["progress"] = 100
        JOBS_STORE[job_id]["message"] = "Vídeo gerado com sucesso!"
        JOBS_STORE[job_id]["output_video"] = str(final_video_path)

    except Exception as e:
        JOBS_STORE[job_id]["status"] = "failed"
        JOBS_STORE[job_id]["message"] = f"Erro no processamento: {str(e)}"
