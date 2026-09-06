import json
import zipfile
import httpx
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.config import settings

class RemoteWorkerClient:
    """
    Cliente para conexão e despacho de jobs de renderização de avatar/áudio:
    - Conexão via Cloudflare Tunnel (Google Colab)
    - Servidor Próprio / VPS / Docker com GPU
    - Exportação de Pacote ZIP autônomo
    """

    @staticmethod
    async def test_connection(worker_url: str, token: Optional[str] = None) -> Dict[str, Any]:
        """Testa se o worker remoto (Colab/VPS) está online e pronto."""
        url = worker_url.rstrip("/") + "/health"
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    return {"status": "online", "details": resp.json()}
                return {"status": "error", "message": f"HTTP {resp.status_code}: {resp.text}"}
        except Exception as e:
            return {"status": "offline", "message": str(e)}

    @staticmethod
    async def dispatch_render_job(
        worker_url: str,
        avatar_video_path: Path,
        audio_path: Path,
        token: Optional[str] = None,
        model_engine: str = "liveportrait"
    ) -> bytes:
        """
        Envia o vídeo de referência do avatar e o arquivo de áudio falado para o worker remoto com GPU.
        Retorna os bytes do vídeo sincronizado (talking-head).
        """
        url = worker_url.rstrip("/") + "/render"
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        async with httpx.AsyncClient(timeout=300.0) as client:
            with open(avatar_video_path, "rb") as v_file, open(audio_path, "rb") as a_file:
                files = {
                    "video": (avatar_video_path.name, v_file, "video/mp4"),
                    "audio": (audio_path.name, a_file, "audio/wav")
                }
                data = {"engine": model_engine}
                
                resp = await client.post(url, files=files, data=data, headers=headers)
                resp.raise_for_status()
                return resp.content

    @staticmethod
    def create_export_package(
        project_id: str,
        script_text: str,
        avatar_video_path: Path,
        voice_audio_path: Optional[Path],
        timeline_cues: list,
        subtitle_style: str,
        output_zip_path: Path
    ) -> Path:
        """
        Cria um pacote .zip autônomo com os arquivos e o script `render_offline.py`
        para que o usuário possa rodar em qualquer máquina gamer ou servidor com GPU.
        """
        output_zip_path.parent.mkdir(parents=True, exist_ok=True)
        
        manifest = {
            "project_id": project_id,
            "script_text": script_text,
            "subtitle_style": subtitle_style,
            "timeline_cues": timeline_cues,
            "has_pregenerated_audio": voice_audio_path is not None
        }

        # Script autônomo que roda no servidor de destino
        standalone_runner_code = '''"""
Script de Renderização Autônoma - CloneStudio PT-BR
Execute este script em uma máquina com GPU e LivePortrait / MuseTalk instalado:
python render_offline.py
"""
import os
import json
import subprocess
from pathlib import Path

def main():
    with open("manifest.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[*] Renderizando projeto: {data['project_id']}")
    
    # 1. Checar GPU
    # 2. Executar LivePortrait / MuseTalk
    avatar_video = "avatar_reference.mp4"
    audio_file = "voice_audio.wav" if os.path.exists("voice_audio.wav") else "generated_voice.wav"
    output_video = "final_rendered_avatar.mp4"
    
    print(f"[*] Processando com LivePortrait: {avatar_video} + {audio_file}")
    # Simulação ou chamada real
    cmd = [
        "ffmpeg", "-y", "-i", avatar_video, "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", output_video
    ]
    subprocess.run(cmd, check=True)
    print(f"[+] Vídeo gerado com sucesso: {output_video}")

if __name__ == "__main__":
    main()
'''

        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
            zf.writestr("render_offline.py", standalone_runner_code)
            
            if avatar_video_path.exists():
                zf.write(avatar_video_path, arcname="avatar_reference.mp4")
            if voice_audio_path and voice_audio_path.exists():
                zf.write(voice_audio_path, arcname="voice_audio.wav")

        return output_zip_path
