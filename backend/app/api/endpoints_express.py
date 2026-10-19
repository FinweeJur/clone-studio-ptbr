import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
try:
    from fastapi import APIRouter, HTTPException
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def post(self, *args, **kwargs): return lambda f: f
        def get(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):
        def __init__(self, status_code, detail=None): self.status_code = status_code; self.detail = detail

from pydantic import BaseModel
from app.core.config import settings
from app.services.trend_radar.niche_presets import NichePresets
from app.services.trend_radar.algorithm_knowledge import AlgorithmKnowledge
from app.services.copy_generator import CopyGenerator
from app.services.thumbnail_generator import ThumbnailGenerator
from app.services.social_publishers.whatsapp_publisher import WhatsAppPublisher

router = APIRouter()

class ExpressVideoRequest(BaseModel):
    clone_id: Optional[str] = None
    niche: Optional[str] = "advocacia"
    topic: Optional[str] = ""
    hook_text: Optional[str] = ""
    target_platforms: Optional[List[str]] = ["instagram", "whatsapp", "tiktok"]
    llm_provider: Optional[str] = "deepseek"

@router.post("/create-auto-video")
async def create_auto_video(req: ExpressVideoRequest):
    """
    Executa o fluxo completo do Modo Piloto Automático em 1 Clique:
    1. Seleciona o Clone ou usa o avatar padrão.
    2. Estrutura o Roteiro Viral em 4 Atos com o Gancho do Nicho.
    3. Calcula o Score de Retenção Algorítmica (Meta/TikTok/Shorts).
    4. Gera automaticamente as Copys para as Redes selecionadas.
    5. Gera a Thumbnail/Capa do Reels (9:16) com o Gancho em destaque.
    6. Fornece links de compartilhamento instantâneo.
    """
    job_id = f"express_{uuid.uuid4().hex[:8]}"
    
    # 1. Carregar clone ou usar padrão
    clone_dir = None
    clone_photo = None
    clone_name = "Avatar Padrão"
    
    if req.clone_id:
        c_path = settings.CLONES_DIR / req.clone_id
        if c_path.exists():
            clone_dir = c_path
            cfg_file = c_path / "config.json"
            if cfg_file.exists():
                try:
                    with open(cfg_file, "r", encoding="utf-8") as f:
                        c_data = json.load(f)
                        clone_name = c_data.get("name", clone_name)
                except Exception:
                    pass
            # Procurar foto/vídeo de referência
            for ext in (".jpg", ".png", ".mp4"):
                matches = list(c_path.glob(f"*{ext}"))
                if matches:
                    clone_photo = matches[0]
                    break

    # Se não houver arquivo específico, usar pasta assets
    if not clone_photo:
        default_assets = list(settings.ASSETS_DIR.glob("*.jpg")) + list(settings.ASSETS_DIR.glob("*.png"))
        if default_assets:
            clone_photo = default_assets[0]

    # 2. Obter gancho e nicho
    niche_key = (req.niche or "advocacia").lower().strip()
    niche_obj = NichePresets.get_niche(niche_key)
    
    if not niche_obj:
        niche_obj = NichePresets.create_custom_niche(niche_key)

    chosen_hook = req.hook_text or (niche_obj["top_profiles"][0]["best_hook"] if niche_obj.get("top_profiles") else "Você sabia que esse detalhe pode mudar tudo?")
    chosen_topic = req.topic or f"Dica essencial de {niche_obj.get('name', niche_key)} que quase ninguém conhece"

    # 3. Montar Roteiro estruturado em 4 Atos com Loop Infinito
    full_script = (
        f"{chosen_hook}\n\n"
        f"Muita gente tem dúvidas sobre {chosen_topic}, mas a verdade que não te contam é simples: "
        f"quando você domina essa regra básica, você economiza tempo e evita prejuízos desnecessários.\n\n"
        f"O grande segredo está em agir antes que o problema aconteça. Guarde isso: documente tudo e consulte um especialista.\n\n"
        f"E é exatamente por isso que você precisa saber que..."
    )

    acts = [
        {
            "act": 1,
            "title": "Gancho Viral (0-3s)",
            "time": "0.0s - 3.5s",
            "content": chosen_hook,
            "visual": "Enquadramento fechado com zoom sutil e texto em destaque amarela bold."
        },
        {
            "act": 2,
            "title": "Retenção & Contexto (3-15s)",
            "time": "3.5s - 15.0s",
            "content": f"Muita gente tem dúvidas sobre {chosen_topic}, mas a verdade que não te contam é simples.",
            "visual": "Avatar gesticulando com cortes de dinamismo a cada 3.2s."
        },
        {
            "act": 3,
            "title": "Momento Aha! / Solução (15-28s)",
            "time": "15.0s - 28.0s",
            "content": "O grande segredo está em agir antes que o problema aconteça. Documente tudo e guarde como prova.",
            "visual": "Ícone gráfico de alerta e documento em destaque na tela."
        },
        {
            "act": 4,
            "title": "Loop Infinito & CTA (28-35s)",
            "time": "28.0s - 35.0s",
            "content": "E é exatamente por isso que você precisa saber que...",
            "visual": "Transição contínua sem quebra de tom para conectar ao primeiro segundo (Retenção 100%+)."
        }
    ]

    # 4. Avaliar Score de Retenção Algorítmica
    audit = AlgorithmKnowledge.audit_script_retention(full_script)

    # 5. Gerar Copys para Redes Sociais
    copies = await CopyGenerator.generate_all_copies(
        script_text=full_script,
        topic=chosen_topic
    )

    # 6. Gerar Capa / Thumbnail (9:16)
    cover_file = None
    if clone_photo:
        try:
            cover_file = ThumbnailGenerator.generate_cover(
                video_or_image_path=clone_photo,
                hook_text=chosen_hook,
                output_name=f"capa_{job_id}.jpg"
            )
        except Exception:
            pass

    # 7. Links rápidos de compartilhamento
    wa_link = WhatsAppPublisher.generate_whatsapp_deep_link(
        caption=copies.get("whatsapp", full_script)
    )
    tg_link = f"https://t.me/share/url?url=&text={wa_link.split('text=')[-1]}"

    return {
        "status": "success",
        "job_id": job_id,
        "clone_name": clone_name,
        "niche": niche_obj.get("name", niche_key),
        "topic": chosen_topic,
        "hook": chosen_hook,
        "script": full_script,
        "acts": acts,
        "audit": audit,
        "copies": copies,
        "thumbnail_url": f"/outputs/capa_{job_id}.jpg" if cover_file and cover_file.exists() else None,
        "quick_share": {
            "whatsapp_link": wa_link,
            "telegram_link": tg_link
        },
        "message": "Vídeo estruturado com sucesso no Modo Piloto Automático!"
    }
