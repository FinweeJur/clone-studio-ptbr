import json
from typing import List, Dict, Any, Optional, AsyncGenerator
try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None
from app.core.config import settings

class UnifiedLLMClient:
    """
    Cliente unificado para conexão com LLMs:
    - DeepSeek (DeepSeek-V3 / DeepSeek-R1 / DeepSeek-Chat)
    - Maritaca AI (MariTalk / Sabiá-3, Sabiá-2 - IA Brasileira)
    - Ollama Local ou Remoto (Llama 3, Qwen 2.5, Mistral)
    - Servidor Customizado Privado (vLLM, LM Studio, LocalAI)
    """

    @staticmethod
    def get_client(
        provider: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> tuple[AsyncOpenAI, str]:
        prov = provider.lower().strip()
        
        if prov == "maritaca":
            key = api_key or settings.MARITACA_API_KEY
            url = base_url or settings.MARITACA_API_URL
            model = settings.MARITACA_MODEL
            # Maritaca AI usa a mesma interface OpenAI compatível
            client = AsyncOpenAI(api_key=key or "maritaca-key", base_url=url)
            return client, model
            
        elif prov == "deepseek":
            key = api_key or settings.DEEPSEEK_API_KEY
            url = base_url or settings.DEEPSEEK_API_URL
            model = settings.DEEPSEEK_MODEL
            client = AsyncOpenAI(api_key=key or "deepseek-key", base_url=url)
            return client, model
            
        elif prov == "ollama":
            key = "ollama"  # Ollama não exige chave
            url = base_url or settings.OLLAMA_API_URL
            model = settings.OLLAMA_MODEL
            client = AsyncOpenAI(api_key=key, base_url=url)
            return client, model
            
        else:  # custom (vLLM, LM Studio, LocalAI)
            key = api_key or settings.CUSTOM_API_KEY or "none"
            url = base_url or settings.CUSTOM_API_URL or "http://localhost:1234/v1"
            model = settings.CUSTOM_MODEL or "custom-model"
            client = AsyncOpenAI(api_key=key, base_url=url)
            return client, model

    @classmethod
    async def generate_completion(
        cls,
        messages: List[Dict[str, str]],
        provider: str = "deepseek",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_override: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        client, default_model = cls.get_client(provider, api_key, base_url)
        model = model_override or default_model
        
        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if response_format:
            kwargs["response_format"] = response_format
            
        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    @classmethod
    async def stream_completion(
        cls,
        messages: List[Dict[str, str]],
        provider: str = "deepseek",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_override: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        client, default_model = cls.get_client(provider, api_key, base_url)
        model = model_override or default_model
        
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    @classmethod
    async def generate_structured_script(
        cls,
        prompt: str,
        template_system_prompt: str,
        provider: str = "deepseek",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gera um roteiro com marcações de B-roll, cartões de texto e pausas no formato JSON estruturado.
        """
        system_instruction = (
            f"{template_system_prompt}\n\n"
            "IMPORTANTE: Retorne ESTRITAMENTE um objeto JSON válido no formato abaixo, sem formatações extras de markdown ou explicações antes/depois:\n"
            "{\n"
            '  "title": "Título do Vídeo",\n'
            '  "estimated_duration_seconds": 45,\n'
            '  "full_spoken_script": "Texto corrido que o clone irá falar...",\n'
            '  "speech_sections": [\n'
            '    {\n'
            '      "order": 1,\n'
            '      "text": "Frase dita pelo avatar com pontuação natural.",\n'
            '      "broll_suggestion": "Descrição visual do que pode aparecer (opcional)",\n'
            '      "text_overlay": "Texto curto para aparecer na tela como apoio (opcional)",\n'
            '      "visual_type": "none | image | text_card | broll_video"\n'
            '    }\n'
            '  ]\n'
            "}"
        )
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]
        
        raw_text = await cls.generate_completion(
            messages=messages,
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            model_override=model_override,
            temperature=0.6,
            response_format={"type": "json_object"} if provider != "maritaca" else None
        )
        
        # Sanitizar caso o modelo inclua blocos ```json ... ```
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except Exception:
            # Fallback seguro
            return {
                "title": "Roteiro Gerado",
                "estimated_duration_seconds": 30,
                "full_spoken_script": raw_text,
                "speech_sections": [
                    {
                        "order": 1,
                        "text": raw_text,
                        "broll_suggestion": None,
                        "text_overlay": None,
                        "visual_type": "none"
                    }
                ]
            }
