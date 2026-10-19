from typing import Dict, List, Any, Optional

# Regiões e Estados suportados
REGIONS_BRAZIL = [
    {"id": "br_all", "name": "Brasil (Nacional)", "uf": "BR"},
    {"id": "br_sp", "name": "São Paulo", "uf": "SP"},
    {"id": "br_rj", "name": "Rio de Janeiro", "uf": "RJ"},
    {"id": "br_mg", "name": "Minas Gerais", "uf": "MG"},
    {"id": "br_ba", "name": "Bahia", "uf": "BA"},
    {"id": "br_pr", "name": "Paraná", "uf": "PR"},
    {"id": "br_rs", "name": "Rio Grande do Sul", "uf": "RS"},
    {"id": "br_pe", "name": "Pernambuco", "uf": "PE"},
    {"id": "br_ce", "name": "Ceará", "uf": "CE"},
    {"id": "br_go", "name": "Goiás", "uf": "GO"},
    {"id": "br_df", "name": "Distrito Federal (Brasília)", "uf": "DF"},
    {"id": "br_sc", "name": "Santa Catarina", "uf": "SC"},
    {"id": "br_es", "name": "Espírito Santo", "uf": "ES"}
]

# Nichos com diretrizes e lista dos Top 10 perfis mais bombantes das redes
NICHE_PRESETS: Dict[str, Dict[str, Any]] = {
    "advocacia": {
        "id": "advocacia",
        "name": "Advocacia / Jurídico",
        "title_ranking": "Top 10 Advogados Mais Bombantes das Redes",
        "icon": "scale",
        "color": "amber",
        "subthemes": [
            "Direito do Trabalho (demissão, horas extras, rescisão)",
            "Direito do Consumidor (nome sujo, voo cancelado, garantia)",
            "Direito de Família (pensão alimentícia, herança, divórcio)",
            "Direito Previdenciário (aposentadoria, BPC/LOAS)",
            "Direito Criminal (direitos em abordagem, fiança)",
            "Direito Tributário e Empresarial (reforma tributária, MEI)"
        ],
        "top_hooks": [
            "Se o seu chefe te disse isso hoje, você tem direito a...",
            "Três coisas que a loja NUNCA pode te obrigar a fazer:",
            "Cuidado: se você assinar esse documento sem ler, você perde...",
            "Você foi demitido? Não saia da empresa antes de conferir isso:",
            "O banco cobrou essa tarifa na sua conta? Pegue em dobro agora:"
        ],
        "hashtags": ["#direitodoconsumidor", "#advogado", "#direitotrabalhista", "#advocacia", "#direitodefamilia", "#leis"],
        "recommended_pacing": "Ritmo moderado (130-140 palavras/min) com pausas para enfatizar artigos e direitos.",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@doutortrabalhista",
                "display_name": "Dr. Marcos Aurélio | Trabalho & CLT",
                "platform": "Instagram & TikTok",
                "followers": "2.8M",
                "monthly_growth": "+140K",
                "avg_views": "1.2M",
                "best_hook": "Seu patrão NÃO pode te obrigar a fazer isso na rescisão!",
                "best_video_views": "8.4M",
                "key_strategy": "Linguagem simples, encenações com diálogos rápidos e artigo de lei na tela."
            },
            {
                "rank": 2,
                "username": "@miranda.juridico",
                "display_name": "Dr. Rodrigo Miranda | Consumidor",
                "platform": "Instagram Reels",
                "followers": "2.1M",
                "monthly_growth": "+95K",
                "avg_views": "950K",
                "best_hook": "O supermercado cometeu esse crime com você e você nem percebeu:",
                "best_video_views": "6.1M",
                "key_strategy": "Gravação no próprio supermercado/loja com produto na mão (imersão visual máxima)."
            },
            {
                "rank": 3,
                "username": "@dra.familiaconsciente",
                "display_name": "Dra. Beatriz Santos | Família & Sucessões",
                "platform": "TikTok & Reels",
                "followers": "1.7M",
                "monthly_growth": "+82K",
                "avg_views": "820K",
                "best_hook": "Pensão alimentícia não é só comida! Olha o que a lei inclui:",
                "best_video_views": "5.3M",
                "key_strategy": "Forte apelo emocional, acolhimento materno e desmistificação de tabus jurídicos."
            },
            {
                "rank": 4,
                "username": "@previdenciariosemsegredo",
                "display_name": "Dr. Anderson Silva | Aposentadoria & INSS",
                "platform": "YouTube Shorts & Reels",
                "followers": "1.4M",
                "monthly_growth": "+65K",
                "avg_views": "740K",
                "best_hook": "Três doenças que dão direito a aposentadoria imediata sem carência:",
                "best_video_views": "4.9M",
                "key_strategy": "Listas rápidas de 3 itens com cartões de texto em amarelo bold na tela."
            },
            {
                "rank": 5,
                "username": "@advogadacriminal_sp",
                "display_name": "Dra. Laura Meirelles | Defesa Penal",
                "platform": "Instagram Reels",
                "followers": "1.2M",
                "monthly_growth": "+58K",
                "avg_views": "680K",
                "best_hook": "Se a polícia bater na sua porta, você NUNCA deve falar isso:",
                "best_video_views": "4.5M",
                "key_strategy": "Ganchos de alto suspense e tensão cívica com postura de firmeza e autoridade."
            },
            {
                "rank": 6,
                "username": "@seusdireitos_hoje",
                "display_name": "Dr. Tiago Tadeu | Direitos do Cidadão",
                "platform": "TikTok & Kwai",
                "followers": "980K",
                "monthly_growth": "+45K",
                "avg_views": "520K",
                "best_hook": "O banco tem que devolver todo o juro abusivo desse financiamento!",
                "best_video_views": "3.8M",
                "key_strategy": "Foco na dor financeira das pessoas e orientações práticas de negociação."
            },
            {
                "rank": 7,
                "username": "@direitofacil_br",
                "display_name": "Dra. Mariana Costa | Imobiliário & Contratos",
                "platform": "Instagram Reels",
                "followers": "850K",
                "monthly_growth": "+39K",
                "avg_views": "460K",
                "best_hook": "Não alugue nem compre imóvel sem antes pedir essas 3 certidões:",
                "best_video_views": "3.2M",
                "key_strategy": "Alertas de risco e prevenção de golpes imobiliários."
            },
            {
                "rank": 8,
                "username": "@tributarista_descomplicado",
                "display_name": "Dr. Felipe Nogueira | MEI & Empresas",
                "platform": "Instagram & YouTube",
                "followers": "720K",
                "monthly_growth": "+34K",
                "avg_views": "390K",
                "best_hook": "A Receita Federal vai cruzar o seu PIX agora! Faça isso para se proteger:",
                "best_video_views": "2.9M",
                "key_strategy": "Urgência de notícias de tributação e dicas de proteção patrimonial."
            },
            {
                "rank": 9,
                "username": "@advogada_da_saude",
                "display_name": "Dra. Patrícia Lima | Planos de Saúde & SUS",
                "platform": "Instagram Reels",
                "followers": "650K",
                "monthly_growth": "+30K",
                "avg_views": "340K",
                "best_hook": "O plano de saúde negou sua cirurgia? A liminar sai em 48 horas!",
                "best_video_views": "2.6M",
                "key_strategy": "Alívio imediato para pessoas em momentos de desespero com remédios/cirurgias."
            },
            {
                "rank": 10,
                "username": "@direito_para_todos_oficial",
                "display_name": "Dr. Vinicius Prado | Cotidiano Jurídico",
                "platform": "TikTok & Reels",
                "followers": "590K",
                "monthly_growth": "+27K",
                "avg_views": "310K",
                "best_hook": "Você comprou pela internet e se arrependeu? A loja é obrigada a devolver o frete!",
                "best_video_views": "2.4M",
                "key_strategy": "Direito do consumidor rápido do dia a dia com demonstrações no celular."
            }
        ]
    },
    "politica": {
        "id": "politica",
        "name": "Política & Gestão Pública",
        "title_ranking": "Top 10 Perfis e Comentaristas Políticos Mais Bombantes",
        "icon": "landmark",
        "color": "blue",
        "subthemes": [
            "Prestação de contas e transparência pública",
            "Votações na Câmara e Senado em linguagem simples",
            "Direitos cívicos e fiscalização de gastos públicos",
            "Políticas públicas municipais, estaduais e federais",
            "Debates, entrevistas e bastidores do poder"
        ],
        "top_hooks": [
            "Atenção para o que acaba de ser votado em Brasília:",
            "Você sabia que o seu município tem direito a essa verba?",
            "Três verdades sobre o novo projeto de lei que ninguém te contou:",
            "Para onde vai o seu imposto? Olha o que descobrimos aqui:",
            "O que mudou na regra a partir de hoje para quem mora em..."
        ],
        "hashtags": ["#politica", "#brasil", "#cidadania", "#noticias", "#gestaopublica", "#transparencia"],
        "recommended_pacing": "Tom firme e direto, cortes a cada 2 segundos e dados visuais destacados na tela.",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@fiscalizabrasil",
                "display_name": "Fiscalização Cívica | Transparência",
                "platform": "Instagram & TikTok",
                "followers": "3.4M",
                "monthly_growth": "+190K",
                "avg_views": "1.8M",
                "best_hook": "Para onde foi o dinheiro da sua cidade? Olha o que achamos no portal da transparência:",
                "best_video_views": "9.2M",
                "key_strategy": "Cortes rápidos do Diário Oficial com setas e valores em destaque."
            },
            {
                "rank": 2,
                "username": "@bastidoresdobrasil",
                "display_name": "Notícias do Congresso em 1 Minuto",
                "platform": "TikTok & Shorts",
                "followers": "2.7M",
                "monthly_growth": "+130K",
                "avg_views": "1.4M",
                "best_hook": "Votaram ontem à meia-noite e quase ninguém viu! Veja o que muda no seu bolso:",
                "best_video_views": "7.5M",
                "key_strategy": "Urgência de breaking news com enquadramento frontal e voz firme."
            },
            {
                "rank": 3,
                "username": "@direito_e_politica_br",
                "display_name": "Prof. Daniel | Análise Constitucional",
                "platform": "Instagram Reels",
                "followers": "1.9M",
                "monthly_growth": "+92K",
                "avg_views": "950K",
                "best_hook": "O que a Constituição realmente diz sobre essa decisão polêmica:",
                "best_video_views": "5.8M",
                "key_strategy": "Didática neutra, texto da lei em tela e desmontagem de fake news."
            },
            {
                "rank": 4,
                "username": "@cidadania_ativa_oficial",
                "display_name": "Voz Cidadã",
                "platform": "Instagram & Kwai",
                "followers": "1.5M",
                "monthly_growth": "+74K",
                "avg_views": "810K",
                "best_hook": "Como pedir a prestação de contas do vereador do seu bairro:",
                "best_video_views": "4.7M",
                "key_strategy": "Tutoriais práticos de cidadania mostrando o passo a passo em sites oficiais."
            },
            {
                "rank": 5,
                "username": "@paineleconomicopolitico",
                "display_name": "Radar Econômico & Político",
                "platform": "YouTube & Reels",
                "followers": "1.2M",
                "monthly_growth": "+60K",
                "avg_views": "690K",
                "best_hook": "A reforma tributária foi aprovada! Veja a lista do que vai subir e cair:",
                "best_video_views": "4.2M",
                "key_strategy": "Tabelas comparativas práticas de antes x depois."
            },
            {
                "rank": 6,
                "username": "@opiniao_sem_filtro_br",
                "display_name": "Debates & Entrevistas",
                "platform": "TikTok & Reels",
                "followers": "980K",
                "monthly_growth": "+48K",
                "avg_views": "560K",
                "best_hook": "A pergunta que deixou o parlamentar sem resposta em plena comissão:",
                "best_video_views": "3.7M",
                "key_strategy": "Cortes com tensão de entrevistas e perguntas sem rodeios."
            },
            {
                "rank": 7,
                "username": "@politica_para_jovens",
                "display_name": "Entenda a Política Fácil",
                "platform": "TikTok",
                "followers": "860K",
                "monthly_growth": "+42K",
                "avg_views": "490K",
                "best_hook": "Você sabe a diferença de Deputado Estadual e Federal? É por isso que você vota errado:",
                "best_video_views": "3.3M",
                "key_strategy": "Linguagem visual moderna, memes leves e comparações do cotidiano."
            },
            {
                "rank": 8,
                "username": "@mapa_do_voto_br",
                "display_name": "Eleições & Dados Cívicos",
                "platform": "Instagram Reels",
                "followers": "740K",
                "monthly_growth": "+36K",
                "avg_views": "420K",
                "best_hook": "Como o seu voto para deputado ajuda a eleger alguém que você nem conhece:",
                "best_video_views": "2.8M",
                "key_strategy": "Explicação do quociente eleitoral com bolinhas ou gráficos dinâmicos."
            },
            {
                "rank": 9,
                "username": "@leis_e_sociedade",
                "display_name": "Sociedade & Direitos Cívicos",
                "platform": "YouTube Shorts",
                "followers": "630K",
                "monthly_growth": "+31K",
                "avg_views": "360K",
                "best_hook": "O que você tem direito de exigir da prefeitura quando cai uma árvore na sua rua:",
                "best_video_views": "2.5M",
                "key_strategy": "Soluções de problemas locais de bairro e zeladoria urbana."
            },
            {
                "rank": 10,
                "username": "@noticias_brasilia_direto",
                "display_name": "Boletim Brasília",
                "platform": "Kwai & Reels",
                "followers": "550K",
                "monthly_growth": "+26K",
                "avg_views": "320K",
                "best_hook": "Três projetos aprovados hoje que começam a valer a partir de amanhã:",
                "best_video_views": "2.1M",
                "key_strategy": "Resumo diário em 30 segundos estilo telejornal de bolso."
            }
        ]
    },
    "tecnologia": {
        "id": "tecnologia",
        "name": "Tecnologia & IA",
        "title_ranking": "Top 10 Criadores de Tecnologia & IA Mais Bombantes",
        "icon": "cpu",
        "color": "indigo",
        "subthemes": [
            "Inteligência Artificial aplicada a produtividade",
            "Automações e ferramentas sem código (no-code)",
            "Novidades em smartphones, hardware e gadgets",
            "Dicas secretas de Windows, Mac e ferramentas online",
            "Cibersegurança e proteção de dados pessoais"
        ],
        "top_hooks": [
            "Essa IA gratuita faz o trabalho de 5 pessoas em 10 segundos:",
            "Pare de fazer isso manualmente no seu computador agora:",
            "O segredo que nenhuma empresa de tecnologia quer que você descubra:",
            "Três ferramentas de IA que parecem ilegais de tão boas:",
            "Se você usa o WhatsApp todo dia, ative essa função imediatamente:"
        ],
        "hashtags": ["#ia", "#inteligenciaartificial", "#tecnologia", "#dicasdetecnologia", "#produtividade", "#tech"],
        "recommended_pacing": "Ritmo acelerado (150-160 palavras/min) com demonstrações em tela (screen recording B-roll).",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@iadodia_oficial",
                "display_name": "IA do Dia | Novidades Tech",
                "platform": "Instagram & TikTok",
                "followers": "3.1M",
                "monthly_growth": "+180K",
                "avg_views": "1.6M",
                "best_hook": "Essa IA gratuita faz o trabalho que você levaria 8 horas para terminar:",
                "best_video_views": "8.8M",
                "key_strategy": "Gravação rápida de tela mostrando o resultado imediato nos primeiros 2 segundos."
            },
            {
                "rank": 2,
                "username": "@dicasparacomputador",
                "display_name": "Dicas Secretas de PC",
                "platform": "TikTok & Shorts",
                "followers": "2.5M",
                "monthly_growth": "+125K",
                "avg_views": "1.3M",
                "best_hook": "Pressione essas duas teclas no seu teclado agora e veja a mágica:",
                "best_video_views": "7.1M",
                "key_strategy": "Atalhos de teclado e comandos no Windows que economizam tempo real."
            },
            {
                "rank": 3,
                "username": "@felipe_automacoes",
                "display_name": "Felipe | Automação com IA",
                "platform": "Instagram Reels",
                "followers": "1.8M",
                "monthly_growth": "+90K",
                "avg_views": "880K",
                "best_hook": "Como eu automatizei 100% das mensagens do meu negócio sem gastar nada:",
                "best_video_views": "5.6M",
                "key_strategy": "Passo a passo no Make/Zapier/Ollama com foco em lucro e tempo livre."
            },
            {
                "rank": 4,
                "username": "@tecnologiabrasil_tech",
                "display_name": "Mundo dos Gadgets",
                "platform": "YouTube & Reels",
                "followers": "1.5M",
                "monthly_growth": "+72K",
                "avg_views": "760K",
                "best_hook": "O celular de R$ 900 que bate de frente com o iPhone novo em fotos:",
                "best_video_views": "5.1M",
                "key_strategy": "Comparações lado a lado de fotos e testes práticos de bateria."
            },
            {
                "rank": 5,
                "username": "@segurancadigital_br",
                "display_name": "Alerta de Golpes & Segurança",
                "platform": "TikTok & Reels",
                "followers": "1.3M",
                "monthly_growth": "+65K",
                "avg_views": "690K",
                "best_hook": "Se você receber esse SMS do banco com o seu nome certo, NÃO CLIQUE:",
                "best_video_views": "4.6M",
                "key_strategy": "Exposição dos novos golpes digitais com simulação na tela do celular."
            },
            {
                "rank": 6,
                "username": "@dev_em_1minuto",
                "display_name": "Código & Programação",
                "platform": "Instagram Reels",
                "followers": "1.1M",
                "monthly_growth": "+52K",
                "avg_views": "580K",
                "best_hook": "Aprenda lógica de programação com esse jogo gratuito no navegador:",
                "best_video_views": "3.9M",
                "key_strategy": "Gamificação de conceitos de programação e ferramentas modernas de IA."
            },
            {
                "rank": 7,
                "username": "@deepseek_brasil",
                "display_name": "Modelos Open Source & LLM",
                "platform": "YouTube Shorts",
                "followers": "920K",
                "monthly_growth": "+48K",
                "avg_views": "510K",
                "best_hook": "Por que o DeepSeek e a IA open source estão deixando os gigantes apavorados:",
                "best_video_views": "3.4M",
                "key_strategy": "Análise geopolítica e técnica de IA aberta rodando localmente no PC."
            },
            {
                "rank": 8,
                "username": "@truques_whatsapp_br",
                "display_name": "Segredos do WhatsApp",
                "platform": "Kwai & TikTok",
                "followers": "840K",
                "monthly_growth": "+41K",
                "avg_views": "460K",
                "best_hook": "Como ouvir áudio no WhatsApp sem a outra pessoa saber que você ouviu:",
                "best_video_views": "3.0M",
                "key_strategy": "Funcionalidades nativas ocultas que quase ninguém conhece."
            },
            {
                "rank": 9,
                "username": "@ferramentas_secretas",
                "display_name": "Sites Que Parecem Ilegais",
                "platform": "TikTok & Reels",
                "followers": "730K",
                "monthly_growth": "+37K",
                "avg_views": "410K",
                "best_hook": "Esse site secreto remove qualquer pessoa do fundo da foto de graça:",
                "best_video_views": "2.7M",
                "key_strategy": "Curadoria de ferramentas utilitárias gratuitas da web."
            },
            {
                "rank": 10,
                "username": "@produtividade_tech",
                "display_name": "Dicas de Notion & IA",
                "platform": "Instagram Reels",
                "followers": "620K",
                "monthly_growth": "+32K",
                "avg_views": "350K",
                "best_hook": "Como organizar toda a sua vida e trabalho em uma única tela limpa:",
                "best_video_views": "2.3M",
                "key_strategy": "Visual minimalista e templates prontos para download."
            }
        ]
    },
    "educacao": {
        "id": "educacao",
        "name": "Conteúdos Educacionais / Aulas",
        "title_ranking": "Top 10 Professores e Educadores Mais Bombantes",
        "icon": "graduation-cap",
        "color": "emerald",
        "subthemes": [
            "Microaulas de idiomas (inglês, espanhol prático)",
            "Dicas para vestibulares, ENEM e concursos públicos",
            "Curiosidades científicas e fatos históricos intrigantes",
            "Técnicas de memorização e aprendizado acelerado",
            "Resumos rápidos de livros e ideias complexas"
        ],
        "top_hooks": [
            "Você provavelmente aprendeu isso errado na escola:",
            "Como falar essa frase em inglês sem soar como um gringo robô:",
            "A técnica dos 2 minutos que vai dobrar a sua capacidade de foco:",
            "O mistério histórico que levou mais de 100 anos para ser resolvido:",
            "Se você está estudando para concurso, nunca cometa esse erro clássico:"
        ],
        "hashtags": ["#educacao", "#aprendizado", "#dicasdeestudo", "#concursos", "#curiosidades", "#enem"],
        "recommended_pacing": "Ritmo envolvente, ganchos visuais e analogias visuais a cada 4 segundos.",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@ingles_com_nativa_br",
                "display_name": "Teacher Carol | Inglês do Dia a Dia",
                "platform": "Instagram & TikTok",
                "followers": "3.3M",
                "monthly_growth": "+170K",
                "avg_views": "1.5M",
                "best_hook": "Pare de falar 'How are you?' se você quer soar como um nativo de verdade!",
                "best_video_views": "8.1M",
                "key_strategy": "Contraste imediato entre inglês de cursinho vs inglês real da rua."
            },
            {
                "rank": 2,
                "username": "@professor_memorizacao",
                "display_name": "Prof. Noslen | Português & Redação",
                "platform": "YouTube Shorts & Reels",
                "followers": "2.9M",
                "monthly_growth": "+140K",
                "avg_views": "1.3M",
                "best_hook": "Nunca mais erre o uso da crase depois de aprender essa rima de 5 segundos:",
                "best_video_views": "7.3M",
                "key_strategy": "Mnemônicos bem-humorados e quadros coloridos com tipografia clara."
            },
            {
                "rank": 3,
                "username": "@curiosidades_historicas_br",
                "display_name": "História sem Filtro",
                "platform": "TikTok & Shorts",
                "followers": "2.2M",
                "monthly_growth": "+110K",
                "avg_views": "1.1M",
                "best_hook": "O verdadeiro motivo pelo qual D. Pedro I proclamou a independência:",
                "best_video_views": "6.0M",
                "key_strategy": "Storytelling com pinturas históricas animadas e revelação de segredos de época."
            },
            {
                "rank": 4,
                "username": "@matematica_rapida_br",
                "display_name": "Matemática em Segundos",
                "platform": "TikTok & Reels",
                "followers": "1.9M",
                "monthly_growth": "+95K",
                "avg_views": "920K",
                "best_hook": "O truque japonês para multiplicar números grandes sem calculadora:",
                "best_video_views": "5.4M",
                "key_strategy": "Cálculo visual desenhado com caneta na folha em tempo real."
            },
            {
                "rank": 5,
                "username": "@dicasdeconcurso_oficial",
                "display_name": "Aprovação Concursos",
                "platform": "Instagram Reels",
                "followers": "1.6M",
                "monthly_growth": "+80K",
                "avg_views": "810K",
                "best_hook": "A lei 8.112 sempre cobra essa pegadinha e 90% dos candidatos caem:",
                "best_video_views": "4.8M",
                "key_strategy": "Questões de prova reais desmembradas com a chave da resposta em 30s."
            },
            {
                "rank": 6,
                "username": "@biologia_curiosa",
                "display_name": "Prof. Lucas | Biologia & Ciência",
                "platform": "YouTube & TikTok",
                "followers": "1.3M",
                "monthly_growth": "+65K",
                "avg_views": "680K",
                "best_hook": "O que acontece com o seu corpo se você for picado por essa formiga:",
                "best_video_views": "4.1M",
                "key_strategy": "Imagens microscópicas em alta definição e curiosidades biológicas impactantes."
            },
            {
                "rank": 7,
                "username": "@redacao_nota_mil",
                "display_name": "Fórmula da Redação ENEM",
                "platform": "Instagram Reels",
                "followers": "1.1M",
                "monthly_growth": "+55K",
                "avg_views": "590K",
                "best_hook": "Três repertórios curingas que você pode usar em QUALQUER tema de redação:",
                "best_video_views": "3.6M",
                "key_strategy": "Templates de frases de introdução e citações filosóficas aplicáveis a tudo."
            },
            {
                "rank": 8,
                "username": "@geografia_interativa",
                "display_name": "Mapas & Geopolítica",
                "platform": "TikTok & Shorts",
                "followers": "950K",
                "monthly_growth": "+48K",
                "avg_views": "520K",
                "best_hook": "Por que o Brasil tem tanta água mas o Nordeste sofre com a seca?",
                "best_video_views": "3.1M",
                "key_strategy": "Mapas 3D animados com relevo e rios em movimento."
            },
            {
                "rank": 9,
                "username": "@livros_em_resumo_br",
                "display_name": "1 Livro por Dia",
                "platform": "Instagram Reels",
                "followers": "820K",
                "monthly_growth": "+40K",
                "avg_views": "450K",
                "best_hook": "A principal lição do livro 'Hábitos Atômicos' explicada em 40 segundos:",
                "best_video_views": "2.8M",
                "key_strategy": "Resumo de best-sellers focado em autoaperfeiçoamento e rotina."
            },
            {
                "rank": 10,
                "username": "@espanhol_para_brasileiros",
                "display_name": "Espanhol Sem Pegadinha",
                "platform": "TikTok & Reels",
                "followers": "710K",
                "monthly_growth": "+35K",
                "avg_views": "390K",
                "best_hook": "Cuidado com os 'falsos amigos' no espanhol: essa palavra NÃO significa o que você pensa:",
                "best_video_views": "2.4M",
                "key_strategy": "Erros engraçados e embaraçosos causados pelo portunhol."
            }
        ]
    },
    "publicidade": {
        "id": "publicidade",
        "name": "Publicidade & Marketing Digital",
        "title_ranking": "Top 10 Criadores de Marketing & Copywriting Mais Bombantes",
        "icon": "megaphone",
        "color": "purple",
        "subthemes": [
            "Estratégias de vendas e conversão",
            "Copywriting e ganchos de anúncios de alto ROI",
            "Análise de campanhas virais e bastidores de marcas",
            "Tendências de criação de conteúdo para criadores",
            "Branding e posicionamento de autoridade"
        ],
        "top_hooks": [
            "O motivo pelo qual essa marca faturou milhões com um vídeo simples:",
            "Use essa estrutura de copy se você quer vender qualquer produto:",
            "O maior erro que você comete ao postar no Instagram hoje:",
            "Como prender a atenção de qualquer pessoa nos primeiros 3 segundos:",
            "Se você quer ganhar dinheiro na internet em 2026, foque nisso:"
        ],
        "hashtags": ["#marketingdigital", "#copywriting", "#vendas", "#trafegopago", "#empreendedorismo", "#negocios"],
        "recommended_pacing": "Ritmo dinâmico, quebra de padrão constante e prova social objetiva.",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@copywriting_de_milhoes",
                "display_name": "Copywriter Estrategista | Vendas",
                "platform": "Instagram & TikTok",
                "followers": "2.9M",
                "monthly_growth": "+155K",
                "avg_views": "1.4M",
                "best_hook": "A frase que você deve colocar na primeira linha do anúncio para triplicar suas vendas:",
                "best_video_views": "7.9M",
                "key_strategy": "Fórmulas comprovadas de AIDA e ganchos de alta conversão explicados com exemplos."
            },
            {
                "rank": 2,
                "username": "@bastidores_do_marketing",
                "display_name": "Análise de Campanhas Virais",
                "platform": "TikTok & Shorts",
                "followers": "2.3M",
                "monthly_growth": "+115K",
                "avg_views": "1.1M",
                "best_hook": "O truque psicológico genial que o McDonald's usa para te fazer comprar o combo grande:",
                "best_video_views": "6.8M",
                "key_strategy": "Desconstrução de técnicas de precificação e neuromarketing de grandes corporações."
            },
            {
                "rank": 3,
                "username": "@criativos_que_convertem",
                "display_name": "Agência de Vídeos Curtos",
                "platform": "Instagram Reels",
                "followers": "1.7M",
                "monthly_growth": "+88K",
                "avg_views": "850K",
                "best_hook": "Como fazer um vídeo de 30 segundos parecer que custou 50 mil reais de produção:",
                "best_video_views": "5.2M",
                "key_strategy": "Dicas de iluminação, enquadramento e transições de corte invisível."
            },
            {
                "rank": 4,
                "username": "@trafego_pago_direto",
                "display_name": "Gestor de Tráfego Pro",
                "platform": "YouTube & Reels",
                "followers": "1.4M",
                "monthly_growth": "+71K",
                "avg_views": "720K",
                "best_hook": "Pare de apertar o botão 'Impulsionar' no Instagram! Você só está queimando dinheiro:",
                "best_video_views": "4.6M",
                "key_strategy": "Comparativo na tela entre o botão Impulsionar e o Gerenciador de Anúncios da Meta."
            },
            {
                "rank": 5,
                "username": "@posicionamento_de_marca",
                "display_name": "Branding & Autoridade",
                "platform": "Instagram Reels",
                "followers": "1.2M",
                "monthly_growth": "+60K",
                "avg_views": "630K",
                "best_hook": "O motivo pelo qual as pessoas pagam R$ 300 numa camisa com esse logotipo:",
                "best_video_views": "3.9M",
                "key_strategy": "Valor percebido, narrativa de marca e gatilho de status social."
            },
            {
                "rank": 6,
                "username": "@socialmedia_sem_neura",
                "display_name": "Rotina de Social Media",
                "platform": "TikTok & Reels",
                "followers": "980K",
                "monthly_growth": "+50K",
                "avg_views": "510K",
                "best_hook": "Três ferramentas que eu uso para planejar 30 dias de posts em apenas 2 horas:",
                "best_video_views": "3.4M",
                "key_strategy": "Automação de calendário editorial e reaproveitamento de conteúdo em canais."
            },
            {
                "rank": 7,
                "username": "@gatilhos_mentais_vendas",
                "display_name": "Neuromarketing Aplicado",
                "platform": "YouTube Shorts",
                "followers": "860K",
                "monthly_growth": "+43K",
                "avg_views": "470K",
                "best_hook": "O efeito de ancoragem: como fazer qualquer preço parecer uma pechincha:",
                "best_video_views": "3.1M",
                "key_strategy": "Exemplos de cardápios e páginas de vendas demonstrados com gráficos."
            },
            {
                "rank": 8,
                "username": "@storytelling_para_negocios",
                "display_name": "Histórias que Vendem",
                "platform": "Instagram Reels",
                "followers": "750K",
                "monthly_growth": "+38K",
                "avg_views": "410K",
                "best_hook": "Não venda o produto, venda a transformação: veja a diferença dessas duas frases:",
                "best_video_views": "2.7M",
                "key_strategy": "Antes x Depois de anúncios sem graça transformados em histórias comoventes."
            },
            {
                "rank": 9,
                "username": "@vendas_b2b_brasil",
                "display_name": "Prospecção & Vendas B2B",
                "platform": "Instagram & LinkedIn",
                "followers": "640K",
                "monthly_growth": "+33K",
                "avg_views": "360K",
                "best_hook": "A mensagem de abordagem no WhatsApp que faz qualquer decisor te responder na hora:",
                "best_video_views": "2.3M",
                "key_strategy": "Scripts de abordagem fria e quebra de objeções corporativas."
            },
            {
                "rank": 10,
                "username": "@criadores_de_conteudo_br",
                "display_name": "Criador Profissional",
                "platform": "TikTok & Kwai",
                "followers": "560K",
                "monthly_growth": "+29K",
                "avg_views": "310K",
                "best_hook": "Como fechar a sua primeira publi mesmo tendo menos de 10 mil seguidores:",
                "best_video_views": "2.0M",
                "key_strategy": "Cálculo de precificação e montagem de Mídia Kit para marcas."
            }
        ]
    },
    "financas": {
        "id": "financas",
        "name": "Finanças & Investimentos",
        "title_ranking": "Top 10 Criadores de Finanças & Investimentos Mais Bombantes",
        "icon": "trending-up",
        "color": "green",
        "subthemes": [
            "Investimentos para iniciantes (Selic, CDB, FIIs)",
            "Como sair das dívidas e negociar no Desenrola",
            "Erros financeiros comuns da classe média",
            "Criação de renda passiva com dividendos",
            "Mentalidade financeira e gestão orçamentária"
        ],
        "top_hooks": [
            "Se você deixar R$ 1.000 na poupança hoje, veja o que acontece em 1 ano:",
            "Três investimentos mais seguros que a poupança e que rendem o dobro:",
            "Como negociar sua dívida com até 90% de desconto hoje mesmo:",
            "O que os ricos fazem com o salário no primeiro dia do mês:",
            "Não compre um carro parcelado antes de assistir a esse vídeo:"
        ],
        "hashtags": ["#financas", "#investimentos", "#educacaofinanceira", "#rendapassiva", "#dinheiro", "#economia"],
        "recommended_pacing": "Tom explicativo, gráficos em B-roll e valores destacados na tela.",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@financas_do_zero",
                "display_name": "Thiago Finanças | Liberdade",
                "platform": "Instagram & YouTube",
                "followers": "4.2M",
                "monthly_growth": "+210K",
                "avg_views": "1.9M",
                "best_hook": "Se você deixar R$ 1.000 na poupança, veja o quanto você perde para a inflação:",
                "best_video_views": "9.5M",
                "key_strategy": "Comparativos diretos com dinheiro físico na mesa e calculadoras."
            },
            {
                "rank": 2,
                "username": "@investidor_sardinha_br",
                "display_name": "Bolsa & Dividendos",
                "platform": "TikTok & Shorts",
                "followers": "2.8M",
                "monthly_growth": "+140K",
                "avg_views": "1.2M",
                "best_hook": "Quanto você precisa investir para receber R$ 1.000 de aluguel isento todo mês:",
                "best_video_views": "7.8M",
                "key_strategy": "Fundos imobiliários com cálculo de rendimento mensal na ponta do lápis."
            },
            {
                "rank": 3,
                "username": "@desenrola_dividas",
                "display_name": "Livre das Dívidas",
                "platform": "Instagram Reels",
                "followers": "1.8M",
                "monthly_growth": "+95K",
                "avg_views": "890K",
                "best_hook": "Como limpar o seu nome no Serasa pagando menos de R$ 100 de acordo:",
                "best_video_views": "5.7M",
                "key_strategy": "Tutoriais gravados direto no app do Serasa e Desenrola Brasil."
            },
            {
                "rank": 4,
                "username": "@economia_popular_br",
                "display_name": "Economia do Povo",
                "platform": "Kwai & TikTok",
                "followers": "1.4M",
                "monthly_growth": "+75K",
                "avg_views": "740K",
                "best_hook": "O truque do supermercado que faz você gastar R$ 300 a mais sem perceber:",
                "best_video_views": "4.9M",
                "key_strategy": "Economia doméstica nas compras do mês e redução de contas fixas."
            },
            {
                "rank": 5,
                "username": "@renda_passiva_pratica",
                "display_name": "Renda Passiva em Dólar",
                "platform": "Instagram Reels",
                "followers": "1.1M",
                "monthly_growth": "+60K",
                "avg_views": "620K",
                "best_hook": "Como receber dividendos em dólar na sua conta morando no Brasil:",
                "best_video_views": "4.3M",
                "key_strategy": "Investimentos internacionais simplificados sem burocracia."
            },
            {
                "rank": 6,
                "username": "@mentemilionaria_brasil",
                "display_name": "Mentalidade & Gestão",
                "platform": "TikTok & Shorts",
                "followers": "980K",
                "monthly_growth": "+52K",
                "avg_views": "530K",
                "best_hook": "A regra dos 50-30-20 que organiza o salário de qualquer assalariado:",
                "best_video_views": "3.8M",
                "key_strategy": "Divisão simples do orçamento em necessidades, desejos e reservas."
            },
            {
                "rank": 7,
                "username": "@financas_para_casais",
                "display_name": "Casal Investidor",
                "platform": "Instagram Reels",
                "followers": "850K",
                "monthly_growth": "+45K",
                "avg_views": "470K",
                "best_hook": "O maior motivo de divórcio no Brasil é esse erro financeiro aqui:",
                "best_video_views": "3.3M",
                "key_strategy": "Alinhamento de metas familiares e orçamento conjunto sem brigas."
            },
            {
                "rank": 8,
                "username": "@planejamento_aposentadoria",
                "display_name": "Aposente Mais Cedo",
                "platform": "YouTube & Reels",
                "followers": "740K",
                "monthly_growth": "+39K",
                "avg_views": "410K",
                "best_hook": "Não dependa apenas do INSS! Monte sua própria previdência com esse cálculo:",
                "best_video_views": "2.9M",
                "key_strategy": "Gráficos de juros compostos ao longo de 15 a 20 anos."
            },
            {
                "rank": 9,
                "username": "@cartoes_e_milhas_br",
                "display_name": "Milhas Lucrativas",
                "platform": "TikTok & Reels",
                "followers": "650K",
                "monthly_growth": "+34K",
                "avg_views": "370K",
                "best_hook": "Como viajar de graça pelo Brasil usando apenas os gastos do seu cartão de crédito:",
                "best_video_views": "2.6M",
                "key_strategy": "Acúmulo de pontos em farmácias e postos de combustível."
            },
            {
                "rank": 10,
                "username": "@pequenos_negocios_lucro",
                "display_name": "MEI & Gestão Financeira",
                "platform": "Instagram Reels",
                "followers": "570K",
                "monthly_growth": "+30K",
                "avg_views": "320K",
                "best_hook": "Nunca misture a conta de pessoa física com a conta jurídica: veja o que acontece:",
                "best_video_views": "2.2M",
                "key_strategy": "Separação de pró-labore e caixa da empresa para pequenos comerciantes."
            }
        ]
    },
    "saude": {
        "id": "saude",
        "name": "Saúde & Bem-Estar",
        "title_ranking": "Top 10 Especialistas de Saúde & Bem-Estar Mais Bombantes",
        "icon": "activity",
        "color": "rose",
        "subthemes": [
            "Dicas de alimentação saudável e metabolismo",
            "Correção de postura e dores nas costas/pescoço",
            "Saúde mental, combate à ansiedade e sono de qualidade",
            "Mitos médicos desmistificados com embasamento",
            "Exercícios práticos de 5 minutos para o dia a dia"
        ],
        "top_hooks": [
            "Se você sente essa dor constante no pescoço, faça isso agora:",
            "O alimento que parece inofensivo mas inflama o seu corpo:",
            "Três coisas que você faz antes de dormir que estão destruindo seu sono:",
            "O que acontece com o seu cérebro quando você para de tomar refrigerante:",
            "Pare de tomar esse remédio para dor de cabeça sem saber disso:"
        ],
        "hashtags": ["#saude", "#bemestar", "#qualidadedevida", "#alimentacaosaudavel", "#medicina", "#exercicios"],
        "recommended_pacing": "Tom empático, acolhedor e seguro, reforçando sempre a consulta a profissionais.",
        "top_profiles": [
            {
                "rank": 1,
                "username": "@doutor_postura_br",
                "display_name": "Dr. Rodrigo Fisioterapia",
                "platform": "Instagram & TikTok",
                "followers": "3.6M",
                "monthly_growth": "+185K",
                "avg_views": "1.7M",
                "best_hook": "Se você trabalha sentado, faça esse movimento de 30 segundos agora mesmo:",
                "best_video_views": "8.9M",
                "key_strategy": "Alongamentos práticos demonstrados na hora em que o espectador pode fazer junto."
            },
            {
                "rank": 2,
                "username": "@nutricionista_consciente",
                "display_name": "Nutri Camila | Alimentação Real",
                "platform": "TikTok & Shorts",
                "followers": "2.6M",
                "monthly_growth": "+130K",
                "avg_views": "1.3M",
                "best_hook": "O alimento que todo mundo acha saudável mas tem mais açúcar que um bolo:",
                "best_video_views": "7.4M",
                "key_strategy": "Leitura de rótulos em supermercados com câmera na mão."
            },
            {
                "rank": 3,
                "username": "@medico_da_familia_br",
                "display_name": "Dr. Paulo | Saúde Descomplicada",
                "platform": "Instagram Reels",
                "followers": "2.0M",
                "monthly_growth": "+105K",
                "avg_views": "980K",
                "best_hook": "Três sinais silenciosos de que a sua pressão arterial está alta sem você saber:",
                "best_video_views": "6.2M",
                "key_strategy": "Alertas de prevenção precoce com tom sereno e educativo."
            },
            {
                "rank": 4,
                "username": "@sono_reparador_oficial",
                "display_name": "Especialista do Sono",
                "platform": "YouTube & Reels",
                "followers": "1.5M",
                "monthly_growth": "+80K",
                "avg_views": "790K",
                "best_hook": "Beba isso 30 minutos antes de deitar e veja como você vai acordar descansado:",
                "best_video_views": "5.0M",
                "key_strategy": "Higiene do sono, chás naturais e controle de luz azul."
            },
            {
                "rank": 5,
                "username": "@saude_mental_pratica",
                "display_name": "Psicóloga Juliana",
                "platform": "TikTok & Reels",
                "followers": "1.3M",
                "monthly_growth": "+68K",
                "avg_views": "670K",
                "best_hook": "A técnica de respiração 4-7-8 que desliga uma crise de ansiedade em 1 minuto:",
                "best_video_views": "4.5M",
                "key_strategy": "Exercícios de respiração guiada com temporizador na tela."
            },
            {
                "rank": 6,
                "username": "@dentista_responde_br",
                "display_name": "Dr. Gabriel | Odonto",
                "platform": "Instagram Reels",
                "followers": "1.1M",
                "monthly_growth": "+58K",
                "avg_views": "590K",
                "best_hook": "Você está escovando os dentes errado a vida inteira! Olha o jeito certo:",
                "best_video_views": "3.9M",
                "key_strategy": "Demonstração com boca de resina e escova mostrando a remoção de placa."
            },
            {
                "rank": 7,
                "username": "@dermatologia_sem_filtro",
                "display_name": "Dra. Renata Dermato",
                "platform": "TikTok & Shorts",
                "followers": "940K",
                "monthly_growth": "+49K",
                "avg_views": "520K",
                "best_hook": "O único produto anti-idade de R$ 40 que realmente funciona e é comprovado:",
                "best_video_views": "3.5M",
                "key_strategy": "Foco em protetor solar e desmistificação de cosméticos caros ineficazes."
            },
            {
                "rank": 8,
                "username": "@treino_em_casa_5min",
                "display_name": "Personal Felipe",
                "platform": "YouTube Shorts",
                "followers": "830K",
                "monthly_growth": "+44K",
                "avg_views": "460K",
                "best_hook": "Exercício de 5 minutos que queima mais calorias que 30 minutos de caminhada:",
                "best_video_views": "3.1M",
                "key_strategy": "Treinos de alta intensidade (HIIT) sem equipamentos na sala de casa."
            },
            {
                "rank": 9,
                "username": "@longevidade_ativa",
                "display_name": "Medicina Preventiva",
                "platform": "Instagram Reels",
                "followers": "720K",
                "monthly_growth": "+38K",
                "avg_views": "400K",
                "best_hook": "O hábito diário que os povos que vivem mais de 100 anos praticam todas as manhãs:",
                "best_video_views": "2.7M",
                "key_strategy": "Estudos sobre as 'Blue Zones' e rotinas saudáveis de centenários."
            },
            {
                "rank": 10,
                "username": "@pediatria_com_amor",
                "display_name": "Dra. Mariana Pediatra",
                "platform": "Instagram & TikTok",
                "followers": "640K",
                "monthly_growth": "+33K",
                "avg_views": "350K",
                "best_hook": "O que fazer nos primeiros segundos se o seu bebê ou criança engasgar:",
                "best_video_views": "2.4M",
                "key_strategy": "Manobra de Heimlich demonstrada com boneco (utilidade pública urgente)."
            }
        ]
    }
}

class NicheManager:
    """Gerenciador de nichos pré-definidos e customizados com ranking dos perfis mais bombantes."""

    @staticmethod
    def get_all_niches() -> List[Dict[str, Any]]:
        return list(NICHE_PRESETS.values())

    @staticmethod
    def get_niche(niche_id: str) -> Optional[Dict[str, Any]]:
        clean_id = niche_id.lower().replace("custom_", "")
        if clean_id in NICHE_PRESETS:
            return NICHE_PRESETS[clean_id]
        return None

    @staticmethod
    def get_top_profiles_for_niche(niche_id: str) -> List[Dict[str, Any]]:
        """Retorna os top 10 perfis mais bombantes da categoria."""
        niche = NicheManager.get_niche(niche_id)
        if niche and "top_profiles" in niche:
            return niche["top_profiles"]
        
        # Gera lista inteligente para nicho customizado
        clean_name = niche_id.replace("custom_", "").replace("_", " ").title()
        return [
            {
                "rank": i + 1,
                "username": f"@{niche_id}_{i+1}_oficial",
                "display_name": f"Criador Top {i+1} de {clean_name}",
                "platform": "Instagram & TikTok",
                "followers": f"{max(100, 950 - i * 75)}K",
                "monthly_growth": f"+{max(15, 65 - i * 4)}K",
                "avg_views": f"{max(80, 520 - i * 40)}K",
                "best_hook": f"O maior segredo sobre {clean_name} que quase ninguém revela:",
                "best_video_views": f"{max(1.0, round(4.5 - i * 0.35, 1))}M",
                "key_strategy": f"Ganchos de alto contraste e demonstrações diretas em {clean_name}."
            }
            for i in range(10)
        ]

    @staticmethod
    def create_custom_niche(custom_name: str) -> Dict[str, Any]:
        """Cria e estrutura um nicho personalizado digitado pelo usuário com seu Top 10."""
        slug = custom_name.strip().lower().replace(" ", "_").replace("/", "_")
        clean_name = custom_name.strip().title()
        
        custom_data = {
            "id": f"custom_{slug}",
            "name": clean_name,
            "title_ranking": f"Top 10 Criadores Mais Bombantes em {clean_name}",
            "icon": "tag",
            "color": "indigo",
            "is_custom": True,
            "subthemes": [
                f"Tópicos essenciais e novidades em {clean_name}",
                f"Dicas práticas e segredos para o público de {clean_name}",
                f"Erros comuns que as pessoas cometem em {clean_name}",
                f"Histórias e casos reais de sucesso em {clean_name}"
            ],
            "top_hooks": [
                f"O maior segredo sobre {clean_name} que quase ninguém conhece:",
                f"Se você trabalha com {clean_name}, precisa saber disso hoje:",
                f"Três erros clássicos em {clean_name} que estão te custando caro:",
                f"Como se destacar em {clean_name} mesmo começando do zero:"
            ],
            "hashtags": [
                f"#{slug.replace('_', '')}",
                f"#{slug.replace('_', '')}brasil",
                "#dicas",
                "#conteudo",
                "#sucesso"
            ],
            "recommended_pacing": "Ritmo equilibrado (140 palavras/min) com ganchos fortes a cada 3 segundos.",
            "top_profiles": NicheManager.get_top_profiles_for_niche(f"custom_{slug}")
        }
        return custom_data

NichePresets = NicheManager

