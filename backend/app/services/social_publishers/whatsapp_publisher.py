import os
import base64
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import httpx
except ImportError:
    httpx = None

class WhatsAppPublisher:
    """
    Publicador unificado para WhatsApp:
    1. Meta WhatsApp Cloud API Oficial (Empresarial, zero risco de ban)
    2. Evolution API (Open Source via QR Code local ou Docker)
    3. WhatsApp Web Direct Share Link (1-Clique sem configuração)
    """

    @classmethod
    async def send_video_cloud_api(
        cls,
        phone_number_id: str,
        access_token: str,
        recipient_number: str,
        video_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia vídeo usando a WhatsApp Cloud API Oficial da Meta:
        POST https://graph.facebook.com/v20.0/{phone_number_id}/messages
        """
        # Formata número (DDI 55 Brasil se necessário)
        clean_num = recipient_number.replace("+", "").replace("-", "").replace(" ", "").strip()
        if len(clean_num) in (10, 11) and not clean_num.startswith("55"):
            clean_num = f"55{clean_num}"

        endpoint = f"https://graph.facebook.com/v20.0/{phone_number_id.strip()}/messages"
        headers = {
            "Authorization": f"Bearer {access_token.strip()}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_num,
            "type": "video",
            "video": {
                "link": video_url,
                "caption": caption or ""
            }
        }

        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"status": "success", "response": data, "message": "Vídeo enviado com sucesso via WhatsApp Cloud API Oficial!"}
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="ignore")
            try:
                err = json.loads(raw)
            except Exception:
                err = raw
            return {"status": "error", "message": f"Erro Meta Cloud API (HTTP {e.code}): {err}"}
        except Exception as e:
            return {"status": "error", "message": f"Falha no envio WhatsApp Cloud API: {str(e)}"}

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
        clean_num = recipient_number.replace("+", "").replace("-", "").replace(" ", "").strip()
        if len(clean_num) in (10, 11) and not clean_num.startswith("55"):
            clean_num = f"55{clean_num}"

        if not video_path.exists():
            return {"status": "error", "message": "Arquivo de vídeo não encontrado."}

        with open(video_path, "rb") as f:
            encoded_media = base64.b64encode(f.read()).decode("utf-8")

        url = f"{api_url.rstrip('/')}/message/sendMedia/{instance_name.strip()}"
        headers = {
            "apikey": api_key.strip(),
            "Content-Type": "application/json"
        }

        payload = {
            "number": clean_num,
            "mediatype": "video",
            "mimetype": "video/mp4",
            "caption": caption or "",
            "media": encoded_media,
            "fileName": video_path.name
        }

        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"status": "success", "response": data, "message": "Vídeo enviado com sucesso via Evolution API!"}
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="ignore")
            return {"status": "error", "message": f"HTTP {e.code} da Evolution API: {raw}"}
        except Exception as e:
            return {"status": "error", "message": f"Erro de conexão com Evolution API: {str(e)}"}

    @staticmethod
    def generate_whatsapp_deep_link(caption: str, phone_number: Optional[str] = None) -> str:
        """Gera link rápido para abrir no WhatsApp Web / Celular com a copy pré-digitada."""
        import urllib.parse
        encoded_text = urllib.parse.quote(caption)
        if phone_number:
            clean_num = phone_number.replace("+", "").replace("-", "").replace(" ", "")
            return f"https://api.whatsapp.com/send?phone={clean_num}&text={encoded_text}"
        return f"https://api.whatsapp.com/send?text={encoded_text}"
