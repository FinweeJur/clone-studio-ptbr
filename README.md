# 🎬 CloneStudio PT-BR - Estúdio Open Source de Clones Digitais com IA

O **CloneStudio PT-BR** é uma solução completa, modular e open source para criação de vídeos com clones digitais hiper-realistas (aprendendo seu **rosto**, **voz** e **estilo**) a partir de roteiros de texto em Português do Brasil.

O aplicativo foi projetado especificamente para rodar de forma fluida mesmo em **computadores modestos** através de uma arquitetura híbrida inteligente.

---

## 🌟 Principais Recursos

1. **Leve e Otimizado para PCs Modestos:**
   - Interface Web moderna (Tailwind CSS) e backend FastAPI que consomem menos de 150MB de RAM.
   - Todo o processamento pesado de IA (Talking Head e Clonagem de Voz) pode ser executado na GPU gratuita do Google Colab ou servidor remoto com 1 clique via **Cloudflare Tunnel**.

2. **Integração Unificada com LLMs:**
   - 🇧🇷 **Maritaca AI** (*MariTalk / Sabiá-3*): IA nacional treinada com cultura e linguagem brasileira.
   - 🇨🇳 **DeepSeek** (*V3 / R1*): Geração de roteiros de alta densidade e raciocínio.
   - 💻 **Ollama Local**: Execução 100% offline e privada (*Qwen 2.5, Llama 3, Mistral*).
   - 🌐 Qualquer endpoint compatível com a API da OpenAI.

3. **Roteirizador com Modo Misto:**
   - **Templates Prontos em PT-BR**: Shorts/Reels Virais (30s e 60s), Vídeos Explicativos/Aulas (90s), Pitch de Vendas Comercial (45s), Boletim de Notícias e Storytelling Pessoal.
   - **Revisor Gramatical e Ortográfico PT-BR**: Garante acentuação e concordância impecáveis na tela.
   - **Chat Copilot**: Bate-papo interativo para reescrever, encurtar ou adicionar ganchos.

4. **Motor de Legendas Inteligentes (5 Estilos Selecionáveis):**
   - **Viral Bold (Hormozi)**: Amarelo vibrante com borda preta espessa.
   - **Karaokê Dinâmico**: Palavra por palavra iluminada em verde neon.
   - **Minimalista Clean**: Branco elegante sem serifa.
   - **Boxed News / Dark Card**: Card escuro corporativo com cantos arredondados.
   - **Gradiente Moderno**: Estilo neon cyberpunk.
   - **Algoritmo Anti-Órfão**: Proíbe quebra de palavras e impede preposições/conjunções soltas (*de, da, com, para, que*) no final de linha.

5. **Timeline de Pós-Produção & B-Roll:**
   - Inserção de imagens sobrepostas, cortes de B-Roll e cartões de texto de apoio.
   - Upload de Trilha Sonora (BGM) com **Auto-Ducking** automático (baixa o volume da música sempre que a voz fala).
   - Seletor de proporção de tela: **9:16 (Shorts/Reels)**, **16:9 (YouTube/Aulas)** e **1:1 (Feed)**.

6. **Opções Flexíveis de Renderização:**
   - **Google Colab com 1 Clique (Cloudflare Tunnel)**: Sem necessidade de abrir portas ou IP público.
   - **Servidor Próprio / VPS / Docker com GPU**: Conecte sua máquina gamer ou servidor dedicado.
   - **Exportação de Pacote ZIP**: Gera um arquivo `.zip` autônomo com script `render_offline.py` para processar em lote onde quiser.

---

## 🚀 Como Iniciar

### 1. Iniciar o Aplicativo Local
Dê um duplo clique no arquivo:
```cmd
start_app.bat
```
Ou pelo terminal:
```cmd
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
O navegador abrirá automaticamente em **`http://localhost:8000`**.

---

### 2. Conectar com a GPU Gratuita do Google Colab (Recomendado para PCs Modestos)
1. Abra o arquivo `worker_colab/CloneStudio_Colab_Worker.ipynb` no [Google Colab](https://colab.research.google.com/).
2. Defina o ambiente de execução para **GPU T4** (*Ambiente de Execução > Alterar tipo de ambiente de execução*).
3. Execute a célula.
4. Ao final, copie a URL gerada (ex: `https://xxxx.trycloudflare.com`).
5. No CloneStudio (aba **Configurações & Worker**), cole a URL e clique em **Testar Conexão**. Pronto!

---

## 📁 Estrutura do Projeto

```
c:/DevCoder/clone-studio-ptbr/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints de Clones, LLMs, Timeline e Render
│   │   ├── core/         # Configurações e Cliente Unificado OpenAI/Maritaca/DeepSeek/Ollama
│   │   ├── services/     # Gerador de Legendas (.ass), Mixador de Áudio BGM e B-Roll
│   │   ├── static/       # Interface Web Moderna (SPA Tailwind)
│   │   └── templates/    # Templates estruturados para o público brasileiro
│   ├── requirements.txt
│   └── run_backend.bat
├── worker_colab/
│   ├── CloneStudio_Colab_Worker.ipynb  # Notebook oficial para Colab + Cloudflare Tunnel
│   └── worker_fastapi.py               # Servidor que roda na GPU remota
├── start_app.bat         # Inicializador 1-clique
└── README.md
```
