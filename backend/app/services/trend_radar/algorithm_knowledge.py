import re
from typing import Dict, List, Any

# Diretrizes Oficiais e Declarações dos Líderes das Redes Sociais
OFFICIAL_ALGORITHM_INSIGHTS = [
    {
        "platform": "Instagram / Meta",
        "source": "Adam Mosseri (Head do Instagram) & Meta for Creators",
        "date_note": "Diretriz Vigente de Distribuição",
        "key_rule": "Envios por Mensagem Privada (DM) e Taxa de Conclusão",
        "details": (
            "Adam Mosseri confirmou categoricamente que o sinal nº 1 de distribuição do algoritmo é o 'Sends per Reach' "
            "(quantas pessoas compartilham o vídeo por DM com amigos). Em seguida vem o tempo médio de visualização e "
            "vídeos 100% originais com rosto humano. Vídeos com marca d'água de outras redes são rebaixados."
        ),
        "ideal_duration": "30 a 60 segundos",
        "format": "9:16 Vertical (1080x1920) com áudio de alta clareza",
        "top_factor": "Compartilhamento por DM / Salvos"
    },
    {
        "platform": "TikTok",
        "source": "TikTok Creator Portal & Algoritmo FYP",
        "date_note": "Modelo de Coortes & Retenção de Loop",
        "key_rule": "Taxa de Conclusão (Completion Rate) e Re-assistidas (Loop)",
        "details": (
            "O algoritmo testa o vídeo inicialmente com 200 a 500 pessoas. Se a taxa de conclusão for superior a 60% e "
            "a porcentagem média ultrapassar 100% (pessoas que assistiram mais de uma vez devido ao loop perfeito), "
            "o vídeo é promovido para a coorte seguinte (5.000 -> 50.000 -> Milhões). Os primeiros 2 segundos decidem "
            "se o usuário passa direto (Swipe-away)."
        ),
        "ideal_duration": "25 a 45 segundos para máxima taxa de loop",
        "format": "9:16 Vertical, legendas dinâmicas e ganchos de corte rápido",
        "top_factor": "Conclusão Total + Rewatch Rate"
    },
    {
        "platform": "YouTube Shorts",
        "source": "Creator Insider & Neal Mohan (CEO do YouTube)",
        "date_note": "Métrica 'Viewed vs Swiped Away'",
        "key_rule": "Proporção de Visualização vs Descarte (VVSA)",
        "details": (
            "O Shorts prioriza a métrica 'Viewed vs Swiped Away'. Para um Short entrar na prateleira viral contínua, "
            "pelo menos 75% a 80% das pessoas no feed devem escolher assistir em vez de rolar. O tempo total assistido "
            "(Watch Time) é somado à autoridade do canal no nicho."
        ),
        "ideal_duration": "40 a 55 segundos",
        "format": "9:16 Vertical com capa atraente e primeiros 3 segundos intensos",
        "top_factor": "Viewed vs Swiped Away (> 75%)"
    },
    {
        "platform": "Kwai",
        "source": "Kwai Creators Brasil",
        "date_note": "Engajamento Relacional & Comentários",
        "key_rule": "Histórias Humanizadas e Debate nos Comentários",
        "details": (
            "O público brasileiro no Kwai prioriza conexões emocionais diretas, histórias do cotidiano e debates "
            "calorosos nos comentários. Fazer perguntas polêmicas ou pedir a opinião explícita dos espectadores na legenda "
            "multiplica as recomendações no feed de Descoberta."
        ),
        "ideal_duration": "30 a 60 segundos",
        "format": "Linguagem simples, sem formalidades excessivas e com rosto visível",
        "top_factor": "Volume de Comentários e Compartilhamentos"
    }
]

# Matriz dos 5 Gatilhos Psicológicos de Retenção
PSYCHOLOGICAL_RETENTION_PILLARS = [
    {
        "id": "seamless_loop",
        "name": "Proposta de Loop (Seamless Loop)",
        "objective": "Fazer o usuário assistir mais de 100% do vídeo sem perceber que reiniciou.",
        "how_to_apply": (
            "A última frase do roteiro deve ser o complemento gramatical exato da primeira frase do gancho. "
            "Exemplo: Início = 'O motivo pelo qual todo mundo erra nessa lei...' / Fim = '... e foi exatamente por isso que "
            "aconteceu... [reinicia: O motivo pelo qual todo mundo erra...]'. Elimine pausas longas e respirações no último milissegundo."
        ),
        "algorithm_boost": "+40% a +80% no multiplicador de entrega da FYP e Reels."
    },
    {
        "id": "familiarity_effect",
        "name": "Efeito de Familiaridade & Identificação",
        "objective": "Criar conexão imediata nos primeiros 2 segundos com o cotidiano do nicho.",
        "how_to_apply": (
            "Comece mencionando o papel exato ou a dor do público-alvo ('Você que é advogado trabalhista...', "
            "'Se você trabalha com vendas...', 'Quem mora em São Paulo sabe...'). O cérebro interrompe o piloto automático "
            "quando ouve sua própria identidade ou situação."
        ),
        "algorithm_boost": "Reduz o 'Swipe-away' inicial em até 65%."
    },
    {
        "id": "pattern_interrupt",
        "name": "Curiosidade & Quebra de Padrão (Pattern Interrupt)",
        "objective": "Reiniciar a janela de atenção do cérebro a cada 2,5 segundos.",
        "how_to_apply": (
            "Alterne cortes de câmera (zoom in / zoom out sutil), insira cards de texto com cores de alto contraste, "
            "efeito sonoro sutil (whoosh / pop) ou troque a imagem de apoio (B-Roll). O cérebro humano se desliga se a imagem "
            "ficar estática por mais de 3 segundos."
        ),
        "algorithm_boost": "Mantém a curva de retenção plana acima de 70% durante o meio do vídeo."
    },
    {
        "id": "learning_satisfaction",
        "name": "Satisfação pelo Aprendizado (Dopamine Hit)",
        "objective": "Fazer o espectador sentir que ganhou conhecimento prático e acionável imediatamente.",
        "how_to_apply": (
            "Elimine enrolações de introdução. Entregue o segredo ou o passo a passo com clareza cristalina e sem jargões. "
            "Quando a pessoa sente que aprendeu algo que pode aplicar hoje, o impulso imediato é SALVAR e ENVIAR para um amigo."
        ),
        "algorithm_boost": "Dispara o gatilho de 'Salvos' e 'Envios por DM' (sinal nº 1 da Meta)."
    },
    {
        "id": "authority_trigger",
        "name": "Gatilho de Autoridade & Prova Social",
        "objective": "Validar a credibilidade do avatar e eliminar desconfiança.",
        "how_to_apply": (
            "Cite dados específicos, artigos de lei, estatísticas reais, casos práticos ou demonstre a tela em funcionamento. "
            "A autoridade técnica faz a audiência respeitar a recomendação e seguir o perfil para não perder futuras orientações."
        ),
        "algorithm_boost": "Aumenta drasticamente a taxa de conversão de visualizador em seguidor (Follow Conversion)."
    }
]

class AlgorithmIntelligenceEngine:
    """Motor de inteligência algorítmica e auditoria de roteiros."""

    @staticmethod
    def get_official_insights() -> List[Dict[str, Any]]:
        return OFFICIAL_ALGORITHM_INSIGHTS

    @staticmethod
    def get_psychological_pillars() -> List[Dict[str, Any]]:
        return PSYCHOLOGICAL_RETENTION_PILLARS

    @classmethod
    def audit_script(cls, script_text: str, duration_seconds: float = 30.0) -> Dict[str, Any]:
        """
        Audita um roteiro avaliando a presença dos gatilhos algorítmicos oficiais,
        gerando um Retention Score de 0 a 100 e recomendações práticas em PT-BR.
        """
        score = 50
        passed_checks = []
        improvement_tips = []

        words = script_text.strip().split()
        word_count = len(words)
        first_sentence = re.split(r'[.?!]', script_text)[0].strip() if script_text else ""
        first_words = first_sentence.lower()

        # 1. Avaliação do Gancho (Hook nos primeiros segundos)
        hook_triggers = [
            "você sabia", "se você", "pare de", "cuidado", "o segredo",
            "três", "3 coisas", "nunca faça", "não saia", "olha o que",
            "atenção", "como fazer", "por que", "todo mundo"
        ]
        has_hook = any(trigger in first_words for trigger in hook_triggers)
        if has_hook:
            score += 15
            passed_checks.append("Gancho inicial com quebra de padrão detectado nos primeiros segundos.")
        else:
            improvement_tips.append("Inicie com uma pergunta provocativa, negação ou alerta para capturar o espectador nos primeiros 2s.")

        # 2. Avaliação de Ritmo e Extensão de Frases
        sentences = [s.strip() for s in re.split(r'[.?!]', script_text) if s.strip()]
        avg_sentence_len = (word_count / len(sentences)) if sentences else 0
        if 5 <= avg_sentence_len <= 15:
            score += 15
            passed_checks.append("Ritmo dinâmico: frases curtas e ideais para fala fluida e pausas do avatar.")
        else:
            improvement_tips.append("Divida frases longas em sentenças mais curtas para permitir pausas naturais e cortes de edição.")

        # 3. Gatilho de Familiaridade / Identificação
        familiarity_keywords = ["você", "sua", "seu", "gente", "todo mundo", "trabalho", "casa", "dinheiro", "dia a dia"]
        has_familiarity = any(k in script_text.lower() for k in familiarity_keywords)
        if has_familiarity:
            score += 10
            passed_checks.append("Efeito de Familiaridade: diálogo direto com o espectador ('você/seu').")
        else:
            improvement_tips.append("Use pronomes diretos ('você', 'seu chefe', 'sua conta') para criar empatia instantânea.")

        # 4. Potencial de Compartilhamento (Shareability)
        share_keywords = ["compartilhe", "mande para", "envie", "salva", "amigo", "dica", "segredo", "lei", "direito"]
        has_share_incentive = any(k in script_text.lower() for k in share_keywords)
        if has_share_incentive:
            score += 10
            passed_checks.append("Gatilho de Compartilhamento / Salvo presente (prioridade nº 1 nos algoritmos de 2026).")
        else:
            improvement_tips.append("Finalize com uma chamada curta incentivando o salvamento ou envio para quem precisa saber da dica.")

        # Normaliza pontuação
        final_score = min(100, max(20, score))

        # Determina selo de prontidão algorítmica
        if final_score >= 85:
            verdict = "Excelente! Alta probabilidade de retenção e viralização nos algoritmos."
            badge_color = "green"
        elif final_score >= 65:
            verdict = "Bom potencial. Algumas melhorias no gancho ou no loop podem elevar a entrega."
            badge_color = "amber"
        else:
            verdict = "Necessita ajustes antes de renderizar para evitar descarte (Swipe-away) nos primeiros segundos."
            badge_color = "red"

        return {
            "retention_score": final_score,
            "verdict": verdict,
            "badge_color": badge_color,
            "passed_checks": passed_checks,
            "improvement_tips": improvement_tips,
            "estimated_words": word_count,
            "estimated_duration_sec": round((word_count / 140) * 60, 1)
        }
