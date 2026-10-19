import json
from typing import Dict, Any, Optional
from app.core.llm_client import UnifiedLLMClient

class CopyGenerator:
    """
    Gerador de legendas, títulos e hashtags para redes sociais e mensageiros em PT-BR.
    """

    @classmethod
    async def generate_all_copies(
        cls,
        script_text: str,
        topic: str = "",
        provider: str = "deepseek",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gera em uma única chamada estruturada as versões de copy e legendas para:
        - Instagram Reels
        - TikTok
        - Kwai
        - Facebook
        - WhatsApp / Telegram
        - Signal
        """
        system_prompt = (
            "Você é um estrategista sênior de Social Media e Copywriting no Brasil. "
            "A partir do roteiro de um vídeo, gere as melhores versões de textos de postagem para cada plataforma.\n\n"
            "Retorne ESTRITAMENTE um JSON no seguinte formato (sem formatação extra de markdown):\n"
            "{\n"
            '  "instagram": {\n'
            '    "caption": "Texto envolvente com emojis, quebras de linha e CTA no final para comentários.",\n'
            '    "hashtags": ["#ia", "#inteligenciaartificial", "#tecnologia", "#reelsbrasil", "#empreendedorismo"]\n'
            '  },\n'
            '  "tiktok": {\n'
            '    "caption": "Frase curta, impactante e com gancho viral (máx 150 caracteres).",\n'
            '    "hashtags": ["#fyp", "#foryou", "#paravoce", "#viral", "#tech"]\n'
            '  },\n'
            '  "kwai": {\n'
            '    "caption": "Texto chamativo com foco no público brasileiro e alta curiosidade.",\n'
            '    "hashtags": ["#kwaibrasil", "#videoscurtos", "#dicas", "#curiosidades"]\n'
            '  },\n'
            '  "facebook": {\n'
            '    "title": "Título atraente para o vídeo no Facebook",\n'
            '    "caption": "Texto explicativo e direto ao ponto que estimula compartilhamentos."\n'
            '  },\n'
            '  "whatsapp_telegram": {\n'
            '    "message": "*📢 Título em Negrito*\\n\\nMensagem direta e conversacional com destaques em negrito para enviar em grupos ou listas de transmissão.\\n\\n👉 Acesse aqui o link."\n'
            '  },\n'
            '  "signal": {\n'
            '    "message": "Mensagem limpa, direta e sem excessos para envio no Signal."\n'
            '  }\n'
            "}"
        )

        user_content = f"Tema: {topic or 'Vídeo com clone digital'}\nRoteiro falado no vídeo:\n\"\"\"\n{script_text}\n\"\"\""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        first_line = script_text.split("\n")[0] if script_text else "Novo vídeo gerado com IA!"
        fallback_data = {
            "instagram": {
                "caption": f"🚀 {first_line}\n\nO que você achou desse conteúdo? Deixe sua opinião nos comentários! 👇",
                "hashtags": ["#ia", "#inteligenciaartificial", "#reels", "#tecnologia", "#brasil"]
            },
            "tiktok": {
                "caption": f"{first_line[:100]} 🔥",
                "hashtags": ["#fyp", "#foryou", "#viral", "#tech"]
            },
            "kwai": {
                "caption": f"Olha isso! {first_line[:100]}",
                "hashtags": ["#kwaibrasil", "#curiosidades"]
            },
            "facebook": {
                "title": first_line[:60],
                "caption": script_text[:250] + "..."
            },
            "whatsapp": f"*🎬 Novo Vídeo Disponível!*\n\n{first_line}\n\nAssista agora e compartilhe com seus amigos!",
            "telegram": f"*🎬 Novo Vídeo Disponível!*\n\n{first_line}\n\nAssista agora e compartilhe!",
            "whatsapp_telegram": {
                "message": f"*🎬 Novo Vídeo Disponível!*\n\n{first_line}\n\nAssista agora e compartilhe!"
            },
            "signal": {
                "message": f"Vídeo: {first_line}"
            }
        }

        try:
            raw_output = await UnifiedLLMClient.generate_completion(
                messages=messages,
                provider=provider,
                api_key=api_key,
                base_url=base_url,
                temperature=0.7,
                response_format={"type": "json_object"} if provider != "maritaca" else None
            )

            cleaned = raw_output.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            parsed = json.loads(cleaned)
            # Garantir chaves diretas whatsapp e telegram
            if "whatsapp" not in parsed and "whatsapp_telegram" in parsed:
                parsed["whatsapp"] = parsed["whatsapp_telegram"].get("message", "")
            if "telegram" not in parsed and "whatsapp_telegram" in parsed:
                parsed["telegram"] = parsed["whatsapp_telegram"].get("message", "")
            return parsed
        except Exception:
            return fallback_data
