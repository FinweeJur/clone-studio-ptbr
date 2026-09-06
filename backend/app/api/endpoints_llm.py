import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.core.llm_client import UnifiedLLMClient

router = APIRouter()

class GenerateScriptRequest(BaseModel):
    template_id: str
    topic: str
    target_audience: Optional[str] = "Público Geral"
    tone_of_voice: Optional[str] = "Descontraído e Confiante"
    provider: Optional[str] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None

class ChatCopilotRequest(BaseModel):
    messages: List[Dict[str, str]]
    provider: Optional[str] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None

class GrammarCheckRequest(BaseModel):
    text: str
    provider: Optional[str] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None

@router.get("/templates")
async def get_templates():
    """Retorna os templates prontos para criação de vídeos em PT-BR."""
    tpl_file = settings.TEMPLATES_DIR / "prompts_ptbr.json"
    if not tpl_file.exists():
        return {"templates": []}
    with open(tpl_file, "r", encoding="utf-8") as f:
        return json.load(f)

@router.post("/generate-script")
async def generate_script(req: GenerateScriptRequest):
    """Gera um roteiro estruturado com marcações de B-Roll usando a LLM escolhida."""
    tpl_file = settings.TEMPLATES_DIR / "prompts_ptbr.json"
    templates_data = {}
    if tpl_file.exists():
        with open(tpl_file, "r", encoding="utf-8") as f:
            templates_data = json.load(f)
            
    selected_template = next(
        (t for t in templates_data.get("templates", []) if t["id"] == req.template_id),
        None
    )
    
    if not selected_template:
        system_prompt = "Você é um roteirista de vídeos em português do Brasil."
    else:
        system_prompt = selected_template["system_prompt"]

    user_prompt = (
        f"Tema do vídeo: {req.topic}\n"
        f"Público-alvo: {req.target_audience}\n"
        f"Tom de voz: {req.tone_of_voice}\n"
        f"Por favor, crie o roteiro completo em português do Brasil e inclua sugestões de B-roll e textos na tela."
    )

    try:
        result = await UnifiedLLMClient.generate_structured_script(
            prompt=user_prompt,
            template_system_prompt=system_prompt,
            provider=req.provider or "deepseek",
            api_key=req.api_key,
            base_url=req.base_url,
            model_override=req.model
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar LLM: {str(e)}")

@router.post("/chat-copilot")
async def chat_copilot(req: ChatCopilotRequest):
    """Bate-papo conversacional com a LLM para lapidar e reescrever partes do roteiro."""
    system_msg = {
        "role": "system",
        "content": (
            "Você é o Assistente Copilot do CloneStudio PT-BR. "
            "Ajude o usuário a aprimorar, encurtar, reescrever ou sugerir ideias de roteiro em português do Brasil. "
            "Mantenha sempre as respostas diretas, úteis e focadas no formato falado por um avatar em vídeo."
        )
    }
    
    # Injeta a instrução de sistema se não estiver presente
    full_messages = [system_msg] + [m for m in req.messages if m.get("role") != "system"]

    try:
        response_text = await UnifiedLLMClient.generate_completion(
            messages=full_messages,
            provider=req.provider or "deepseek",
            api_key=req.api_key,
            base_url=req.base_url,
            model_override=req.model,
            temperature=0.7
        )
        return {"status": "success", "reply": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no chat copilot: {str(e)}")

@router.post("/check-grammar")
async def check_grammar(req: GrammarCheckRequest):
    """Revisa a gramática e acentuação do texto em PT-BR para evitar erros em tela."""
    messages = [
        {
            "role": "system",
            "content": (
                "Você é um revisor ortográfico e gramatical especialista em Português do Brasil. "
                "Corrija apenas erros de ortografia, pontuação e concordância no texto do roteiro, "
                "mantendo o tom natural e a fluidez falada. Retorne apenas o texto corrigido."
            )
        },
        {"role": "user", "content": req.text}
    ]

    try:
        corrected = await UnifiedLLMClient.generate_completion(
            messages=messages,
            provider=req.provider or "deepseek",
            api_key=req.api_key,
            base_url=req.base_url
        )
        return {"status": "success", "original": req.text, "corrected": corrected.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na revisão: {str(e)}")
