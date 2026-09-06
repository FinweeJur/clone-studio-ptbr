import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.services.subtitle_generator import SubtitleStyle

router = APIRouter()

class TimelineItem(BaseModel):
    id: str
    start: float
    end: float
    type: str  # "image_overlay", "text_card", "broll_video"
    content: str
    media_path: Optional[str] = None

@router.get("/subtitle-styles")
async def get_subtitle_styles():
    """Retorna os 5 estilos de legenda disponíveis."""
    return {
        "styles": [
            {
                "id": SubtitleStyle.HORMOZI,
                "name": "Viral Bold (Hormozi)",
                "description": "Amarelo neon com borda preta grossa e sombra sólida. Máximo impacto em redes sociais.",
                "preview_color": "#FFD700"
            },
            {
                "id": SubtitleStyle.KARAOKE,
                "name": "Karaokê Dinâmico",
                "description": "Texto branco que acende em verde neon conforme cada palavra é pronunciada.",
                "preview_color": "#00FF66"
            },
            {
                "id": SubtitleStyle.MINIMALIST,
                "name": "Minimalista Clean",
                "description": "Branco puro com tipografia elegante sem serifa e leitura sutil.",
                "preview_color": "#FFFFFF"
            },
            {
                "id": SubtitleStyle.BOXED_DARK,
                "name": "Boxed News / Dark Card",
                "description": "Card retangular escuro semitransparente atrás do texto, estilo corporativo/notícias.",
                "preview_color": "#1A1A1A"
            },
            {
                "id": SubtitleStyle.GRADIENT_NEON,
                "name": "Gradiente Moderno",
                "description": "Ciano fluorescente com bordas e brilho moderno estilo cyberpunk.",
                "preview_color": "#00F0FF"
            }
        ]
    }

@router.post("/upload-asset")
async def upload_asset(
    file: UploadFile = File(...),
    asset_type: str = Form("image")  # "image", "bgm", "video"
):
    """Faz upload de uma imagem de B-Roll ou trilha de fundo BGM."""
    asset_id = str(uuid.uuid4())[:8]
    ext = Path(file.filename).suffix
    dest_name = f"{asset_type}_{asset_id}{ext}"
    dest_path = settings.UPLOADS_DIR / dest_name

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "asset_id": asset_id,
        "filename": file.filename,
        "file_path": str(dest_path),
        "url": f"/uploads/{dest_name}"
    }
