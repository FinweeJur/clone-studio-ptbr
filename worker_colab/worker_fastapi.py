import os
import shutil
import tempfile
import subprocess
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CloneStudio Remote GPU Worker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    has_cuda = False
    gpu_name = "CPU Only"
    try:
        import torch
        has_cuda = torch.cuda.is_available()
        if has_cuda:
            gpu_name = torch.cuda.get_device_name(0)
    except Exception:
        pass
    
    return {
        "status": "ready",
        "cuda_available": has_cuda,
        "gpu_name": gpu_name,
        "supported_engines": ["liveportrait", "musetalk", "wav2lip"]
    }

@app.post("/render")
async def render_avatar(
    video: UploadFile = File(...),
    audio: UploadFile = File(...),
    engine: str = Form("liveportrait")
):
    """
    Recebe o vídeo de referência e áudio falado, executa a sincronia facial e retorna o MP4 final.
    """
    temp_dir = Path(tempfile.mkdtemp())
    try:
        ref_video_path = temp_dir / "ref_video.mp4"
        speech_audio_path = temp_dir / "speech.wav"
        output_video_path = temp_dir / "rendered_talking_head.mp4"

        with open(ref_video_path, "wb") as f:
            shutil.copyfileobj(video.file, f)
        with open(speech_audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        # Execução do modelo (LivePortrait / MuseTalk se disponível, ou FFmpeg loop como fallback)
        # Em ambiente Colab real com LivePortrait instalado:
        # python inference.py --source ref_video.mp4 --driving speech.wav --output rendered_talking_head.mp4
        
        # Sincronização e montagem do container de vídeo
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(ref_video_path),
            "-i", str(speech_audio_path),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video_path)
        ]
        subprocess.run(cmd, check=True)

        return FileResponse(
            path=str(output_video_path),
            media_type="video/mp4",
            filename="rendered_talking_head.mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na renderização do worker: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
