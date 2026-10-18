try:
    import httpx
except ImportError:
    httpx = None
from pathlib import Path
from typing import Dict, Any, Optional

class TelegramPublisher:
    """
    Publicador direto via Telegram Bot API (gratuito e sem burocracia).
    Envia arquivos de vídeo MP4 em alta resolução diretamente para canais, grupos ou conversas.
    """

    @staticmethod
    async def send_video(
        bot_token: str,
        chat_id: str,
        video_path: Path,
        caption: Optional[str] = None,
        parse_mode: str = "HTML",
        supports_streaming: bool = True
    ) -> Dict[str, Any]:
        """
        Envia o vídeo para o Telegram usando o endpoint /sendVideo.
        """
        url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
        
        if not video_path.exists():
            return {"status": "error", "message": f"Arquivo de vídeo não encontrado: {video_path}"}

        # Telegram aceita legendas de até 1024 caracteres no sendVideo
        trimmed_caption = (caption or "")[:1024]

        data = {
            "chat_id": chat_id,
            "caption": trimmed_caption,
            "parse_mode": parse_mode,
            "supports_streaming": "true" if supports_streaming else "false"
        }

        async with httpx.AsyncClient(timeout=180.0) as client:
            with open(video_path, "rb") as v_file:
                files = {
                    "video": (video_path.name, v_file, "video/mp4")
                }
                try:
                    resp = await client.post(url, data=data, files=files)
                    res_json = resp.json()
                    if resp.status_code == 200 and res_json.get("ok"):
                        return {
                            "status": "success",
                            "message_id": res_json["result"]["message_id"],
                            "chat": res_json["result"]["chat"]["title"] if "title" in res_json["result"]["chat"] else chat_id
                        }
                    else:
                        return {
                            "status": "error",
                            "message": res_json.get("description", resp.text)
                        }
                except Exception as e:
                    return {"status": "error", "message": f"Falha na conexão com Telegram: {str(e)}"}
