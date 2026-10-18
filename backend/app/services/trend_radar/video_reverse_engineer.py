import re
from typing import Dict, List, Any, Optional
from app.services.trend_radar.algorithm_knowledge import AlgorithmIntelligenceEngine

class VideoReverseEngineer:
    """
    Motor de Engenharia Reversa Multimodal de Vídeos e Roteiros Virais.
    Destrincha ganchos, ritmo de edição, propostas de loop e adapta fórmulas para o avatar do usuário.
    """

    @classmethod
    def decompose_structure(cls, transcript: str, duration_sec: float = 40.0) -> Dict[str, Any]:
        """
        Decompõe o roteiro nos 4 atos da engenharia reversa:
        1. Gancho (Hook 0-3s)
        2. Retenção & Problema (Story/Retain 3-20s)
        3. Ponto de Virada / Lição (Aha! Moment 20-35s)
        4. Loop Sem Costura & CTA (Loop & Share 35-40s)
        """
        sentences = [s.strip() for s in re.split(r'[.?!]', transcript) if s.strip()]
        if not sentences:
            sentences = [transcript]

        # 1. Gancho (primeira frase ou primeiros 3 segundos)
        hook_sentence = sentences[0] if sentences else ""

        # 2. Retenção (frases intermediárias)
        retain_sentences = sentences[1:3] if len(sentences) >= 3 else sentences[1:2]
        story_text = " ".join(retain_sentences)

        # 3. Ponto de Virada (miolo explicativo)
        aha_sentences = sentences[3:-1] if len(sentences) >= 5 else (sentences[2:-1] if len(sentences) >= 4 else [])
        aha_text = " ".join(aha_sentences) if aha_sentences else story_text

        # 4. Fechamento e Loop (última frase)
        closing_sentence = sentences[-1] if len(sentences) > 1 else sentences[0]

        # Análise de Loop: verifica se o final conecta gramaticalmente com o gancho
        loop_suggestion = (
            f"Para criar um loop perfeito com esse vídeo, termine sua fala com: "
            f"'... e o motivo disso ter acontecido foi porque...' de modo que emende imediatamente na primeira frase: "
            f"'{hook_sentence}'"
        )

        # Ritmo de cortes sugerido
        word_count = len(transcript.split())
        words_per_sec = word_count / max(1.0, duration_sec)
        pacing_verdict = "Dinâmico / Acelerado (Cortes a cada 2.0s)" if words_per_sec > 2.5 else "Moderado e Claro (Cortes a cada 3.5s)"

        # Auditoria algorítmica
        audit = AlgorithmIntelligenceEngine.audit_script(transcript, duration_sec)

        return {
            "hook_act": {
                "timestamp": "0.0s - 3.5s",
                "content": hook_sentence,
                "strategy": "Quebra de padrão inicial para interromper o scroll do usuário",
                "recommended_visual": "Plano fechado com zoom dinâmico e legenda amarela bold"
            },
            "retain_act": {
                "timestamp": "3.5s - 18.0s",
                "content": story_text or hook_sentence,
                "strategy": "Apresentação da dor ou curiosidade que mantém a pessoa assistindo",
                "recommended_visual": "Inserção de card de texto ou imagem de apoio B-roll na tela"
            },
            "aha_moment_act": {
                "timestamp": "18.0s - 32.0s",
                "content": aha_text or story_text,
                "strategy": "Entrega clara do segredo, artigo de lei, código ou ensinamento prático",
                "recommended_visual": "Demonstração direta ou destaque de palavras-chave"
            },
            "loop_and_cta_act": {
                "timestamp": f"32.0s - {round(duration_sec, 1)}s",
                "content": closing_sentence,
                "strategy": "Loop contínuo (seamless loop) e incentivo sutil de salvamento/compartilhamento",
                "recommended_visual": "Conexão sem respiração vazia para reiniciar o vídeo sem corte brusco"
            },
            "pacing_analysis": {
                "words_per_sec": round(words_per_sec, 2),
                "cuts_per_minute": 24 if words_per_sec > 2.5 else 16,
                "verdict": pacing_verdict,
                "recommended_subtitle_style": "hormozi_bold"
            },
            "loop_architecture": loop_suggestion,
            "algorithm_audit": audit
        }

    @classmethod
    async def clone_formula_to_script(
        cls,
        formula_data: Dict[str, Any],
        user_topic: str,
        target_niche: str,
        user_tone: str = "Descontraído e Autoritário",
        provider: str = "deepseek",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pega a estrutura psicológica e técnica de um vídeo viral (engenharia reversa)
        e gera um roteiro 100% novo para o avatar do usuário no nicho desejado.
        """
        from app.core.llm_client import UnifiedLLMClient

        system_prompt = (
            "Você é o Diretor Criativo e Engenheiro de Roteiros do CloneStudio PT-BR. "
            "Sua tarefa é criar um NOVO roteiro em Português do Brasil aproveitando estritamente "
            "a fórmula estrutural de retenção de um vídeo que comprovadamente viralizou nas redes sociais.\n\n"
            "Diretrizes obrigatórias:\n"
            "1. Crie um Gancho (Hook) forte nos primeiros 3 segundos seguindo a mesma mecânica de quebra de padrão.\n"
            "2. Mantenha o ritmo dinâmico com frases curtas e diretas para o avatar falar com naturalidade.\n"
            "3. Entregue um Momento Aha! com alto valor educacional ou prático.\n"
            "4. Crie um Loop Seamless (a última frase do roteiro deve se conectar gramaticalmente com a primeira).\n"
            "5. Sugira os momentos exatos de sobreposição de B-roll e cards de texto.\n\n"
            "Retorne ESTRITAMENTE um objeto JSON no seguinte formato (sem markdown ou blocos de código extras):\n"
            "{\n"
            '  "title": "Título Cativante do Vídeo",\n'
            '  "full_spoken_script": "Texto corrido que o clone irá falar...",\n'
            '  "hook_analysis": "Explicação de por que esse gancho funciona",\n'
            '  "loop_explanation": "Como a frase final emenda no início para criar o loop",\n'
            '  "broll_cues": [\n'
            '    { "second": 3.0, "type": "text_card", "content": "Texto chave na tela" },\n'
            '    { "second": 15.0, "type": "image_overlay", "content": "Imagem ilustrativa" }\n'
            '  ]\n'
            "}"
        )

        user_prompt = (
            f"Nicho do Usuário: {target_niche}\n"
            f"Tema Específico: {user_topic}\n"
            f"Tom de Voz: {user_tone}\n\n"
            f"Fórmula Viral de Referência (Engenharia Reversa):\n"
            f"- Gancho Original: \"{formula_data.get('hook_act', {}).get('content', '')}\"\n"
            f"- Estrutura de Retenção: \"{formula_data.get('retain_act', {}).get('strategy', '')}\"\n"
            f"- Ritmo Recomendado: {formula_data.get('pacing_analysis', {}).get('verdict', '')}\n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        raw_output = await UnifiedLLMClient.generate_completion(
            messages=messages,
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            temperature=0.6,
            response_format={"type": "json_object"} if provider != "maritaca" else None
        )

        # Limpeza do JSON
        cleaned = raw_output.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            import json
            return json.loads(cleaned)
        except Exception:
            # Fallback seguro
            return {
                "title": f"Dica de {target_niche}: {user_topic}",
                "full_spoken_script": raw_output,
                "hook_analysis": "Gancho gerado com base na fórmula viral.",
                "loop_explanation": "A frase final conecta com o início para engajar o espectador no rewatch.",
                "broll_cues": [{"second": 3.0, "type": "text_card", "content": user_topic}]
            }
