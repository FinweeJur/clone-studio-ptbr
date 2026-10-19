import json
from pathlib import Path
from typing import Dict, Any, Optional, List
try:
    from fastapi import APIRouter, HTTPException
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):
        def __init__(self, status_code, detail=None): self.status_code = status_code; self.detail = detail

from pydantic import BaseModel
from app.core.config import settings
from app.services.connection_tester import ConnectionTester

router = APIRouter()

CONFIG_CONNECTIONS_FILE = settings.DATA_DIR / "connections_config.json"

def load_connections_config() -> Dict[str, Any]:
    if not CONFIG_CONNECTIONS_FILE.exists():
        return {
            "llm_provider": "deepseek",
            "deepseek_api_key": "",
            "deepseek_base_url": "https://api.deepseek.com/v1",
            "deepseek_model": "deepseek-chat",
            "maritaca_api_key": "",
            "maritaca_base_url": "https://chat.maritaca.ai/api",
            "maritaca_model": "sabia-3",
            "ollama_base_url": "http://localhost:11434/v1",
            "ollama_model": "qwen2.5:7b",
            "custom_api_key": "",
            "custom_base_url": "http://localhost:1234/v1",
            "custom_model": "custom-model",
            "whatsapp_type": "evolution", # 'cloud' ou 'evolution'
            "whatsapp_cloud_phone_number_id": "",
            "whatsapp_cloud_access_token": "",
            "whatsapp_cloud_waba_id": "",
            "whatsapp_evolution_api_url": "http://localhost:8080",
            "whatsapp_evolution_api_key": "",
            "whatsapp_evolution_instance": "",
            "meta_access_token": "",
            "meta_selected_instagram_id": "",
            "meta_selected_page_id": "",
            "telegram_bot_token": "",
            "telegram_chat_id": "",
            "worker_url": "",
            "worker_token": ""
        }
    try:
        with open(CONFIG_CONNECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_connections_config(data: Dict[str, Any]):
    with open(CONFIG_CONNECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Schemas
class TestLlmRequest(BaseModel):
    provider: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None

class TestWhatsAppCloudRequest(BaseModel):
    phone_number_id: str
    access_token: str
    waba_id: Optional[str] = None

class TestWhatsAppEvolutionRequest(BaseModel):
    api_url: str
    api_key: str
    instance_name: Optional[str] = None

class TestMetaGraphRequest(BaseModel):
    access_token: str

class TestTelegramRequest(BaseModel):
    bot_token: str
    chat_id: Optional[str] = None

@router.get("/status")
def get_status():
    """Retorna o estado atual das conexões configuradas."""
    return {"status": "success", "config": load_connections_config()}

@router.get("/hardware-profile")
def get_hardware_profile():
    """Detecta automaticamente se a máquina é um PC Leve ou Potente."""
    profile = ConnectionTester.detect_local_hardware()
    return {"status": "success", "profile": profile}

@router.get("/presets")
def get_presets():
    """Retorna os presets de configuração rápida para DeepSeek, Maritaca AI e Ollama."""
    return {
        "status": "success",
        "llm_presets": {
            "deepseek": {
                "name": "DeepSeek (V3 / R1)",
                "base_url": "https://api.deepseek.com/v1",
                "model": "deepseek-chat",
                "description": "Excelente raciocínio, muito rápido e custo extremamente acessível."
            },
            "maritaca": {
                "name": "Maritaca AI (Sabiá-3)",
                "base_url": "https://chat.maritaca.ai/api",
                "model": "sabia-3",
                "description": "IA 100% Brasileira desenvolvida pela Unicamp, perfeita para expressões e leis do Brasil."
            },
            "ollama": {
                "name": "Ollama Local (Offline)",
                "base_url": "http://localhost:11434/v1",
                "model": "qwen2.5:7b",
                "description": "100% gratuito, privado e offline direto no seu computador."
            },
            "custom": {
                "name": "Servidor Local / Privado (vLLM, LM Studio)",
                "base_url": "http://localhost:1234/v1",
                "model": "custom-model",
                "description": "Conecte a qualquer servidor local compatível com a API de Chat."
            }
        }
    }

@router.post("/test-llm")
def test_llm(req: TestLlmRequest):
    """Testa a conexão com o provedor de IA com micro-ping."""
    res = ConnectionTester.test_llm_connection(
        provider=req.provider,
        api_key=req.api_key,
        base_url=req.base_url,
        model=req.model
    )
    return res

@router.post("/test-whatsapp-cloud")
def test_whatsapp_cloud(req: TestWhatsAppCloudRequest):
    """Testa credenciais da WhatsApp Cloud API Oficial."""
    res = ConnectionTester.test_whatsapp_cloud_api(
        phone_number_id=req.phone_number_id,
        access_token=req.access_token,
        waba_id=req.waba_id
    )
    return res

@router.post("/test-whatsapp-evolution")
def test_whatsapp_evolution(req: TestWhatsAppEvolutionRequest):
    """Testa conexão com Evolution API Open Source."""
    res = ConnectionTester.test_whatsapp_evolution_api(
        api_url=req.api_url,
        api_key=req.api_key,
        instance_name=req.instance_name
    )
    return res

@router.post("/test-meta-graph")
def test_meta_graph(req: TestMetaGraphRequest):
    """Testa o token da Meta e auto-descobre contas do Instagram e Facebook."""
    res = ConnectionTester.test_meta_graph_api(access_token=req.access_token)
    return res

@router.post("/test-telegram")
def test_telegram(req: TestTelegramRequest):
    """Testa o Bot do Telegram."""
    res = ConnectionTester.test_telegram_bot(bot_token=req.bot_token, chat_id=req.chat_id)
    return res

@router.post("/save-all")
def save_all(data: Dict[str, Any]):
    """Persiste todas as configurações e chaves de conexões com segurança local."""
    save_connections_config(data)
    return {"status": "success", "message": "Configurações salvas com sucesso!"}
