import httpx
from pathlib import Path
from typing import Dict, Any, Optional

class KwaiPublisher:
    """
    Publicador para Kwai Open Platform API.
    """

    API_BASE = "https://open.kwai.com/openapi"

    @classmethod
    async def publish_video(
        cls,
        access_token: str,
        video_path: Path,
        caption: str
    ) -> Dict[str, Any]:
        """
        Publica um vídeo curto na conta Kwai do criador.
        """
        if not video_path.exists():
            return {"status": "error", "message": "Arquivo de vídeo não encontrado."}

        url = f"{cls.API_BASE}/video/upload"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                with open(video_path, "rb") as f:
                    files = {"video": (video_path.name, f, "video/mp4")}
                    data = {"caption": caption[:200]}
                    resp = await client.post(url, headers=headers, files=files, data=data)
                    res_data = resp.json()
                    if resp.status_code == 200 and res_data.get("result") == 1:
                        return {"status": "success", "platform": "Kwai", "details": res_data}
                    return {"status": "error", "message": res_data.get("error_msg", f"HTTP {resp.status_code}")}
            except Exception as e:
                return {"status": "error", "message": f"Falha na conexão com Kwai: {str(e)}"}
