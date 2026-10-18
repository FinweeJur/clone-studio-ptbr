import asyncio
try:
    import httpx
except ImportError:
    httpx = None
from pathlib import Path
from typing import Dict, Any, Optional

class MetaPublisher:
    """
    Publicador oficial para Instagram Reels e Facebook Reels via Meta Graph API v20.0+.
    """

    GRAPH_API_URL = "https://graph.facebook.com/v20.0"

    @classmethod
    async def publish_instagram_reels(
        cls,
        access_token: str,
        ig_user_id: str,
        video_public_url: str,
        caption: str,
        cover_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fluxo oficial em 2 etapas para Reels no Instagram:
        1. Criação do container de mídia: POST /{ig-user-id}/media (media_type=REELS)
        2. Publicação: POST /{ig-user-id}/media_publish
        """
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 1. Iniciar Container de Vídeo
                container_params = {
                    "access_token": access_token,
                    "media_type": "REELS",
                    "video_url": video_public_url,
                    "caption": caption
                }
                if cover_url:
                    container_params["cover_url"] = cover_url

                init_resp = await client.post(f"{cls.GRAPH_API_URL}/{ig_user_id}/media", data=container_params)
                init_data = init_resp.json()
                
                if "id" not in init_data:
                    return {"status": "error", "message": init_data.get("error", {}).get("message", "Falha ao criar container no Instagram")}

                container_id = init_data["id"]

                # 2. Aguardar processamento do vídeo pela Meta (Polling de status)
                status_ok = False
                for _ in range(20):
                    await asyncio.sleep(5)
                    status_resp = await client.get(
                        f"{cls.GRAPH_API_URL}/{container_id}",
                        params={"fields": "status_code", "access_token": access_token}
                    )
                    status_data = status_resp.json()
                    if status_data.get("status_code") == "FINISHED":
                        status_ok = True
                        break
                    elif status_data.get("status_code") == "ERROR":
                        return {"status": "error", "message": "A Meta reportou erro ao processar o vídeo do Reels."}

                if not status_ok:
                    return {"status": "error", "message": "Tempo limite excedido no processamento do vídeo pela Meta."}

                # 3. Publicar Container
                pub_resp = await client.post(
                    f"{cls.GRAPH_API_URL}/{ig_user_id}/media_publish",
                    data={"creation_id": container_id, "access_token": access_token}
                )
                pub_data = pub_resp.json()

                if "id" in pub_data:
                    return {"status": "success", "media_id": pub_data["id"], "platform": "Instagram Reels"}
                return {"status": "error", "message": pub_data.get("error", {}).get("message", "Erro ao publicar Reels.")}

            except Exception as e:
                return {"status": "error", "message": f"Erro de comunicação com Meta API: {str(e)}"}

    @classmethod
    async def publish_facebook_reels(
        cls,
        access_token: str,
        page_id: str,
        video_public_url: str,
        title: str,
        description: str
    ) -> Dict[str, Any]:
        """
        Publica um vídeo de Reels em uma Página do Facebook.
        """
        url = f"{cls.GRAPH_API_URL}/{page_id}/videos"
        data = {
            "access_token": access_token,
            "file_url": video_public_url,
            "title": title,
            "description": description
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(url, data=data)
                res_data = resp.json()
                if "id" in res_data:
                    return {"status": "success", "video_id": res_data["id"], "platform": "Facebook Reels"}
                return {"status": "error", "message": res_data.get("error", {}).get("message", "Erro no Facebook Reels")}
            except Exception as e:
                return {"status": "error", "message": str(e)}
