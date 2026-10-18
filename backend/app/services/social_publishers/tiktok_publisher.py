try:
    import httpx
except ImportError:
    httpx = None
from pathlib import Path
from typing import Dict, Any, Optional

class TikTokPublisher:
    """
    Publicador para TikTok via Content Posting API v2.
    """

    API_BASE = "https://open.tiktokapis.com/v2"

    @classmethod
    async def post_video_init(
        cls,
        access_token: str,
        video_path: Path,
        title: str,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
        disable_duet: bool = False,
        disable_stitch: bool = False,
        disable_comment: bool = False
    ) -> Dict[str, Any]:
        """
        Inicia a postagem de vídeo no TikTok:
        POST /v2/post/publish/video/init/
        """
        if not video_path.exists():
            return {"status": "error", "message": "Arquivo de vídeo não encontrado."}

        url = f"{cls.API_BASE}/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        video_size = video_path.stat().st_size

        payload = {
            "post_info": {
                "title": title[:150],
                "privacy_level": privacy_level,
                "disable_duet": disable_duet,
                "disable_stitch": disable_stitch,
                "disable_comment": disable_comment
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,
                "total_chunk_count": 1
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                data = resp.json()
                if data.get("error", {}).get("code") == "ok" or "data" in data:
                    upload_url = data["data"]["upload_url"]
                    publish_id = data["data"]["publish_id"]

                    # Upload dos bytes do vídeo para a URL assinada do TikTok
                    with open(video_path, "rb") as f:
                        v_bytes = f.read()
                    
                    up_headers = {
                        "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
                        "Content-Type": "video/mp4"
                    }
                    up_resp = await client.put(upload_url, content=v_bytes, headers=up_headers)
                    if up_resp.status_code in (200, 201):
                        return {"status": "success", "publish_id": publish_id, "platform": "TikTok"}
                    return {"status": "error", "message": f"Erro no upload para TikTok: HTTP {up_resp.status_code}"}

                return {"status": "error", "message": data.get("error", {}).get("message", "Falha ao iniciar postagem no TikTok")}
            except Exception as e:
                return {"status": "error", "message": f"Erro de conexão com TikTok API: {str(e)}"}
