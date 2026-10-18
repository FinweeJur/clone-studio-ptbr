from typing import List, Dict, Any, Optional
try:
    from fastapi import APIRouter, HTTPException
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
        def delete(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):
        def __init__(self, status_code, detail=None): self.status_code = status_code; self.detail = detail
from pydantic import BaseModel

from app.services.trend_radar.niche_presets import NicheManager, REGIONS_BRAZIL, NICHE_PRESETS
from app.services.trend_radar.playwright_inspector import PlaywrightMediaInspector
from app.services.trend_radar.video_reverse_engineer import VideoReverseEngineer
from app.services.trend_radar.algorithm_knowledge import AlgorithmIntelligenceEngine

router = APIRouter()

# Schemas
class CustomNicheRequest(BaseModel):
    name: str

class InspectUrlRequest(BaseModel):
    url: str

class ReverseEngineerRequest(BaseModel):
    transcript: str
    duration_seconds: Optional[float] = 40.0
    title: Optional[str] = "Vídeo Viral Analisado"

class CloneFormulaRequest(BaseModel):
    formula_data: Dict[str, Any]
    user_topic: str
    target_niche: str
    user_tone: Optional[str] = "Descontraído e Autoritário"
    provider: Optional[str] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None

class AuditScriptRequest(BaseModel):
    script_text: str
    duration_seconds: Optional[float] = 30.0

# Endpoints
@router.get("/niches")
async def list_niches():
    """Retorna todos os nichos disponíveis com seus temas e ganchos."""
    return {
        "status": "success",
        "niches": NicheManager.get_all_niches()
    }

@router.post("/custom-niche")
async def create_custom_niche(req: CustomNicheRequest):
    """Cria e estrutura um nicho personalizado digitado pelo usuário com seu Top 10."""
    if not req.name.strip():
        raise HTTPException(status_code=400, detail="Nome do nicho não pode ser vazio.")
    data = NicheManager.create_custom_niche(req.name)
    return {
        "status": "success",
        "niche": data
    }

@router.get("/regions")
async def list_regions():
    """Retorna as regiões e estados brasileiros suportados para filtro."""
    return {
        "status": "success",
        "regions": REGIONS_BRAZIL
    }

@router.get("/top-profiles")
async def get_top_profiles(niche_id: str = "advocacia", region_id: str = "br_all"):
    """Retorna os Top 10 perfis mais bombantes do nicho especificado."""
    profiles = NicheManager.get_top_profiles_for_niche(niche_id)
    niche_obj = NicheManager.get_niche(niche_id)
    ranking_title = niche_obj["title_ranking"] if niche_obj else f"Top 10 Perfis Mais Bombantes em {niche_id}"
    
    return {
        "status": "success",
        "niche_id": niche_id,
        "region_id": region_id,
        "title_ranking": ranking_title,
        "profiles": profiles
    }

@router.post("/inspect-url")
async def inspect_url(req: InspectUrlRequest):
    """Navega via Playwright para inspecionar um vídeo de rede social pública."""
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="URL inválida.")
    result = await PlaywrightMediaInspector.inspect_url(req.url)
    return result

@router.post("/reverse-engineer")
async def reverse_engineer(req: ReverseEngineerRequest):
    """Executa a engenharia reversa de um vídeo/roteiro viral."""
    if not req.transcript.strip():
        raise HTTPException(status_code=400, detail="Texto da transcrição não pode ser vazio.")
    
    breakdown = VideoReverseEngineer.decompose_structure(
        transcript=req.transcript,
        duration_sec=req.duration_seconds or 40.0
    )
    return {
        "status": "success",
        "title": req.title,
        "breakdown": breakdown
    }

@router.post("/clone-formula")
async def clone_formula_to_script(req: CloneFormulaRequest):
    """Gera um roteiro novo para o avatar do usuário baseado na fórmula viral."""
    result = await VideoReverseEngineer.clone_formula_to_script(
        formula_data=req.formula_data,
        user_topic=req.user_topic,
        target_niche=req.target_niche,
        user_tone=req.user_tone or "Descontraído e Autoritário",
        provider=req.provider or "deepseek",
        api_key=req.api_key,
        base_url=req.base_url
    )
    return {
        "status": "success",
        "script_data": result
    }

@router.get("/algorithm-guide")
async def get_algorithm_guide():
    """Retorna as diretrizes oficiais de algoritmos e a matriz dos 5 gatilhos psicológicos."""
    return {
        "status": "success",
        "official_insights": AlgorithmIntelligenceEngine.get_official_insights(),
        "psychological_pillars": AlgorithmIntelligenceEngine.get_psychological_pillars()
    }

@router.post("/audit-script")
async def audit_script(req: AuditScriptRequest):
    """Audita um roteiro avaliando score de retenção algorítmico."""
    result = AlgorithmIntelligenceEngine.audit_script(
        script_text=req.script_text,
        duration_seconds=req.duration_seconds or 30.0
    )
    return {
        "status": "success",
        "audit": result
    }
