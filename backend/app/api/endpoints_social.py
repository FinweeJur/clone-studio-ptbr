import json
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional
try:
    from fastapi import APIRouter, HTTPException, UploadFile, File, Form
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
        def delete(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):
        def __init__(self, status_code, detail=None): self.status_code = status_code; self.detail = detail
    UploadFile = File = Form = Any
from pydantic import BaseModel
from app.core.config import settings
from app.services.copy_generator import CopyGenerator
from app.services.social_publishers.telegram_publisher import TelegramPublisher
from app.services.social_publishers.whatsapp_publisher import WhatsAppPublisher
from app.services.social_publishers.meta_publisher import MetaPublisher
from app.services.social_publishers.tiktok_publisher import TikTokPublisher
from app.services.social_publishers.kwai_publisher import KwaiPublisher
from app.services.social_publishers.signal_publisher import SignalPublisher

router = APIRouter()

SOCIAL_CONFIG_FILE = settings.DATA_DIR / "social_config.json"

def load_social_config() -> Dict[str, Any]:
    if not SOCIAL_CONFIG_FILE.exists():
        return {
            "telegram_bot_token": "",
            "telegram_chat_id": "",
            "whatsapp_api_url": "http://localhost:8080",
            "whatsapp_api_key": "",
            "whatsapp_instance": "",
            "meta_access_token": "",
            "instagram_user_id": "",
            "facebook_page_id": "",
            "tiktok_access_token": "",
            "kwai_access_token": "",
            "signal_api_url": "http://localhost:8080",
            "signal_sender_number": ""
        }
    try:
        with open(SOCIAL_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_social_config(config: Dict[str, Any]):
    with open(SOCIAL_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# Schemas
class GenerateCopiesRequest(BaseModel):
    script_text: str
    topic: Optional[str] = ""
    provider: Optional[str] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None

class ShareLinksRequest(BaseModel):
    caption: str
    video_url: Optional[str] = ""
    phone_number: Optional[str] = None

class TelegramSendRequest(BaseModel):
    video_path: str
    caption: str
    bot_token: Optional[str] = None
    chat_id: Optional[str] = None

class WhatsAppSendRequest(BaseModel):
    video_path: str
    caption: str
    recipient_number: str
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    instance_name: Optional[str] = None

class InstagramReelsRequest(BaseModel):
    video_public_url: str
    caption: str
    access_token: Optional[str] = None
    ig_user_id: Optional[str] = None

class FacebookReelsRequest(BaseModel):
    video_public_url: str
    title: str
    description: str
    access_token: Optional[str] = None
    page_id: Optional[str] = None

class TikTokPublishRequest(BaseModel):
    video_path: str
    title: str
    access_token: Optional[str] = None

class KwaiPublishRequest(BaseModel):
    video_path: str
    caption: str
    access_token: Optional[str] = None

class SignalSendRequest(BaseModel):
    video_path: str
    message: str
    recipients: List[str]
    api_url: Optional[str] = None
    sender_number: Optional[str] = None

# Endpoints
@router.get("/config")
async def get_config():
    """Retorna as configurações e credenciais das redes salvas."""
    return load_social_config()

@router.post("/config")
async def update_config(config: Dict[str, Any]):
    """Atualiza as credenciais das redes salvas."""
    current = load_social_config()
    current.update(config)
    save_social_config(current)
    return {"status": "success", "config": current}

@router.post("/generate-copies")
async def generate_copies(req: GenerateCopiesRequest):
    """Gera copys, títulos e hashtags para todas as redes usando a IA."""
    result = await CopyGenerator.generate_all_copies(
        script_text=req.script_text,
        topic=req.topic or "",
        provider=req.provider or "deepseek",
        api_key=req.api_key,
        base_url=req.base_url
    )
    return {"status": "success", "copies": result}

@router.post("/share-links")
async def get_share_links(req: ShareLinksRequest):
    """Gera links rápidos para compartilhar no WhatsApp e Telegram com 1 clique."""
    wa_link = WhatsAppPublisher.generate_whatsapp_deep_link(req.caption, req.phone_number)
    
    encoded_caption = urllib.parse.quote(req.caption)
    encoded_url = urllib.parse.quote(req.video_url or "")
    tg_link = f"https://t.me/share/url?url={encoded_url}&text={encoded_caption}" if req.video_url else f"https://t.me/share/url?url=&text={encoded_caption}"

    return {
        "whatsapp_link": wa_link,
        "telegram_link": tg_link
    }

@router.post("/telegram/send")
async def send_to_telegram(req: TelegramSendRequest):
    """Envia o vídeo MP4 diretamente para um canal, grupo ou chat do Telegram."""
    cfg = load_social_config()
    token = req.bot_token or cfg.get("telegram_bot_token")
    chat = req.chat_id or cfg.get("telegram_chat_id")

    if not token or not chat:
        raise HTTPException(status_code=400, detail="Token do bot ou Chat ID do Telegram não configurados.")

    res = await TelegramPublisher.send_video(
        bot_token=token,
        chat_id=chat,
        video_path=Path(req.video_path),
        caption=req.caption
    )
    return res

@router.post("/whatsapp/send")
async def send_to_whatsapp(req: WhatsAppSendRequest):
    """Envia o vídeo para o WhatsApp via Evolution API."""
    cfg = load_social_config()
    api_url = req.api_url or cfg.get("whatsapp_api_url")
    api_key = req.api_key or cfg.get("whatsapp_api_key")
    instance = req.instance_name or cfg.get("whatsapp_instance")

    if not api_url or not api_key or not instance:
        raise HTTPException(status_code=400, detail="Configurações da Evolution API incompletas.")

    res = await WhatsAppPublisher.send_video_evolution_api(
        api_url=api_url,
        api_key=api_key,
        instance_name=instance,
        recipient_number=req.recipient_number,
        video_path=Path(req.video_path),
        caption=req.caption
    )
    return res

@router.post("/meta/instagram-reels")
async def publish_instagram(req: InstagramReelsRequest):
    """Publica no Instagram Reels via Meta Graph API."""
    cfg = load_social_config()
    token = req.access_token or cfg.get("meta_access_token")
    ig_id = req.ig_user_id or cfg.get("instagram_user_id")

    if not token or not ig_id:
        raise HTTPException(status_code=400, detail="Token da Meta ou ID do Instagram não configurados.")

    res = await MetaPublisher.publish_instagram_reels(
        access_token=token,
        ig_user_id=ig_id,
        video_public_url=req.video_public_url,
        caption=req.caption
    )
    return res

@router.post("/meta/facebook-reels")
async def publish_facebook(req: FacebookReelsRequest):
    """Publica no Facebook Reels via Meta Graph API."""
    cfg = load_social_config()
    token = req.access_token or cfg.get("meta_access_token")
    page_id = req.page_id or cfg.get("facebook_page_id")

    if not token or not page_id:
        raise HTTPException(status_code=400, detail="Token da Meta ou Page ID do Facebook não configurados.")

    res = await MetaPublisher.publish_facebook_reels(
        access_token=token,
        page_id=page_id,
        video_public_url=req.video_public_url,
        title=req.title,
        description=req.description
    )
    return res

@router.post("/tiktok/publish")
async def publish_tiktok(req: TikTokPublishRequest):
    """Publica no TikTok via Content Posting API."""
    cfg = load_social_config()
    token = req.access_token or cfg.get("tiktok_access_token")

    if not token:
        raise HTTPException(status_code=400, detail="Token do TikTok não configurado.")

    res = await TikTokPublisher.post_video_init(
        access_token=token,
        video_path=Path(req.video_path),
        title=req.title
    )
    return res

@router.post("/kwai/publish")
async def publish_kwai(req: KwaiPublishRequest):
    """Publica no Kwai via Open Platform API."""
    cfg = load_social_config()
    token = req.access_token or cfg.get("kwai_access_token")

    if not token:
        raise HTTPException(status_code=400, detail="Token do Kwai não configurado.")

    res = await KwaiPublisher.publish_video(
        access_token=token,
        video_path=Path(req.video_path),
        caption=req.caption
    )
    return res

@router.post("/signal/send")
async def send_signal(req: SignalSendRequest):
    """Envia vídeo para contatos/grupos no Signal."""
    cfg = load_social_config()
    api_url = req.api_url or cfg.get("signal_api_url")
    sender = req.sender_number or cfg.get("signal_sender_number")

    if not api_url or not sender:
        raise HTTPException(status_code=400, detail="Configurações do Signal incompletas.")

    res = await SignalPublisher.send_video(
        api_url=api_url,
        sender_number=sender,
        recipients=req.recipients,
        video_path=Path(req.video_path),
        message=req.message
    )
    return res
