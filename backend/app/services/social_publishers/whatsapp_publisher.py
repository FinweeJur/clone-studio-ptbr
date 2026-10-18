import base64
try:
    import httpx
except ImportError:
    httpx = None
from pathlib import Path
from typing import Dict, Any, Optional

class WhatsAppPublisher:
    """
    Publicador para WhatsApp com suporte a:
    1. Evolution API (Open Source local/Docker muito popular no Brasil)
    2. Meta WhatsApp Cloud API Oficial
    3. Z-API / Provedores genéricos
    """

    @staticmethod
    async def send_video_evolution_api(
        api_url: str,
        api_key: str,
        instance_name: str,
        recipient_number: str,
        video_path: Path,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia mensagem de vídeo via Evolution API:
        POST /message/sendMedia/{instance}
        """
        url = f"{api_url.rstrip('/')}/message/sendMedia/{instance_name}"
        headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }

        # Formata número (adiciona DDI 55 se brasileiro e sem DDI)
        clean_num = recipient_number.replace("+", "").replace("-", "").replace(" ", "").strip()
        if len(clean_num) in (10, 11) and not clean_num.startswith("55"):
            clean_num = f"55{clean_num}"

        if not video_path.exists():
            return {"status": "error", "message": "Arquivo de vídeo não encontrado."}

        with open(video_path, "rb") as f:
            encoded_media = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "number": clean_num,
            "mediatype": "video",
            "mimetype": "video/mp4",
            "caption": caption or "",
            "media": encoded_media,
            "fileName": video_path.name
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code in (200, 201):
                    return {"status": "success", "response": resp.json()}
                return {"status": "error", "message": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"status": "error", "message": f"Erro de conexão com Evolution API: {str(e)}"}

    @staticmethod
    def generate_whatsapp_deep_link(caption: str, phone_number: Optional[str] = None) -> str:
        """
        Gera um link rápido para abrir no WhatsApp Web / App com o texto já digitado.
        """
        import urllib.parse
        encoded_text = urllib.parse.quote(caption)
        if phone_number:
            clean_num = phone_number.replace("+", "").replace("-", "").replace(" ", "")
            return f"https://api.whatsapp.com/send?phone={clean_num}&text={encoded_text}"
        return f"https://api.whatsapp.com/send?text={encoded_text}"
