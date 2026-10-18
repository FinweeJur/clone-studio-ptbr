import base64
try:
    import httpx
except ImportError:
    httpx = None
from pathlib import Path
from typing import List, Dict, Any, Optional

class SignalPublisher:
    """
    Publicador para Signal via signal-cli REST API.
    """

    @classmethod
    async def send_video(
        cls,
        api_url: str,
        sender_number: str,
        recipients: List[str],
        video_path: Path,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia mensagem com anexo de vídeo para o Signal.
        """
        if not video_path.exists():
            return {"status": "error", "message": "Arquivo de vídeo não encontrado."}

        url = f"{api_url.rstrip('/')}/v2/send"
        
        with open(video_path, "rb") as f:
            base64_attachment = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "number": sender_number,
            "recipients": recipients,
            "message": message or "",
            "base64_attachments": [base64_attachment]
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(url, json=payload)
                if resp.status_code in (200, 201):
                    return {"status": "success", "platform": "Signal", "recipients": recipients}
                return {"status": "error", "message": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"status": "error", "message": f"Erro Signal: {str(e)}"}
