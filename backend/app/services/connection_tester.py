import os
import sys
import time
import json
import platform
import subprocess
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List

class ConnectionTester:
    """
    Testador unificado de conexões para APIs focadas em:
    - DeepSeek (V3 / R1)
    - Maritaca AI (Sabiá-3 - IA Brasileira)
    - Ollama (Local / Offline)
    - Servidor Customizado Privado (vLLM, LM Studio, LocalAI)
    - WhatsApp Oficial (Meta Cloud API) e Open Source (Evolution API)
    - Meta Graph API (Instagram Reels e Facebook)
    - Telegram Bot
    """

    @staticmethod
    def _http_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, data: Optional[Dict[str, Any]] = None, timeout: float = 10.0) -> tuple[int, Any, float]:
        """Faz requisição HTTP resiliente usando urllib da biblioteca padrão do Python."""
        headers = headers or {}
        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                latency_ms = round((time.time() - start_time) * 1000, 1)
                status_code = response.status
                raw = response.read().decode("utf-8", errors="ignore")
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = raw
                return status_code, parsed, latency_ms
        except urllib.error.HTTPError as e:
            latency_ms = round((time.time() - start_time) * 1000, 1)
            raw = e.read().decode("utf-8", errors="ignore")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = raw
            return e.code, parsed, latency_ms
        except Exception as e:
            latency_ms = round((time.time() - start_time) * 1000, 1)
            return 0, str(e), latency_ms

    @classmethod
    def test_llm_connection(
        cls,
        provider: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Testa conexão rápida (1 token) estritamente com DeepSeek, Maritaca AI, Ollama ou Servidor Custom."""
        prov = provider.lower().strip()
        headers = {}
        
        if prov == "maritaca":
            url = (base_url or "https://chat.maritaca.ai/api").rstrip("/") + "/chat/completions"
            m = model or "sabia-3"
            headers["authorization"] = f"Key {api_key}" if api_key else ""
        elif prov == "deepseek":
            url = (base_url or "https://api.deepseek.com/v1").rstrip("/") + "/chat/completions"
            m = model or "deepseek-chat"
            headers["Authorization"] = f"Bearer {api_key}"
        elif prov == "ollama":
            # Para Ollama local, verifica status e modelos instalados
            ollama_base = (base_url or "http://localhost:11434").rstrip("/")
            if ollama_base.endswith("/v1"):
                ollama_base = ollama_base[:-3]
            tags_url = f"{ollama_base}/api/tags"
            code, data, latency = cls._http_request(tags_url, method="GET", timeout=4.0)
            if code == 200 and isinstance(data, dict):
                models = [item.get("name") for item in data.get("models", [])]
                return {
                    "status": "success",
                    "provider": "ollama",
                    "latency_ms": latency,
                    "message": f"Ollama Local conectado! ({len(models)} modelos instalados)",
                    "installed_models": models,
                    "active_model": model or (models[0] if models else "nenhum")
                }
            elif code == 0:
                return {
                    "status": "error",
                    "provider": "ollama",
                    "message": "Ollama não respondeu em http://localhost:11434. Verifique se o aplicativo Ollama está aberto no seu computador.",
                    "hint": "Inicie o Ollama no Windows para usar modelos 100% locais e offline."
                }
            url = (base_url or "http://localhost:11434/v1").rstrip("/") + "/chat/completions"
            m = model or "qwen2.5:7b"
        else: # custom (vLLM, LM Studio, LocalAI)
            url = (base_url or "http://localhost:1234/v1").rstrip("/") + "/chat/completions"
            m = model or "custom-model"
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

        if not api_key and prov not in ("ollama",):
            return {
                "status": "error",
                "provider": prov,
                "message": f"Chave de API não informada para {prov.capitalize()}.",
                "hint": "Insira sua chave de API para testar a conexão."
            }

        payload = {
            "model": m,
            "messages": [{"role": "user", "content": "Olá, responda apenas 'OK'."}],
            "max_tokens": 5,
            "temperature": 0.1
        }

        code, resp, latency = cls._http_request(url, method="POST", headers=headers, data=payload, timeout=12.0)
        
        if code in (200, 201):
            return {
                "status": "success",
                "provider": prov,
                "latency_ms": latency,
                "model": m,
                "message": f"Conexão com {prov.capitalize()} ({m}) validada com sucesso! (Ping: {latency}ms)"
            }
        elif code == 401:
            return {
                "status": "error",
                "provider": prov,
                "message": f"Chave de API inválida para {prov.capitalize()} (HTTP 401).",
                "hint": "Verifique a chave copiada do painel do provedor."
            }
        elif code == 404:
            return {
                "status": "error",
                "provider": prov,
                "message": f"Endpoint não encontrado (HTTP 404): {url}",
                "hint": "Confira a URL base do servidor."
            }
        else:
            err_msg = str(resp) if isinstance(resp, str) else json.dumps(resp)
            return {
                "status": "error",
                "provider": prov,
                "message": f"Erro na conexão com {prov.capitalize()} (HTTP {code}): {err_msg[:200]}",
                "hint": "Verifique se o serviço está ativo ou se há saldo de créditos disponível."
            }

    @classmethod
    def test_whatsapp_cloud_api(
        cls,
        phone_number_id: str,
        access_token: str,
        waba_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Valida credenciais da WhatsApp Cloud API Oficial consultando os dados do número corporativo."""
        if not phone_number_id or not access_token:
            return {
                "status": "error",
                "message": "Informe o Phone Number ID e o Access Token da WhatsApp Cloud API Oficial.",
                "hint": "Obtenha no Meta for Developers > WhatsApp > API Setup."
            }

        url = f"https://graph.facebook.com/v20.0/{phone_number_id.strip()}?fields=verified_name,display_phone_number,quality_rating,code_verification_status"
        headers = {"Authorization": f"Bearer {access_token.strip()}"}
        code, resp, latency = cls._http_request(url, method="GET", headers=headers, timeout=10.0)

        if code == 200 and isinstance(resp, dict):
            return {
                "status": "success",
                "type": "whatsapp_cloud_official",
                "latency_ms": latency,
                "verified_name": resp.get("verified_name", "Verificado"),
                "display_number": resp.get("display_phone_number", ""),
                "quality_rating": resp.get("quality_rating", "GREEN"),
                "message": f"WhatsApp Cloud API Oficial conectado! Número: {resp.get('display_phone_number')} ({resp.get('verified_name')})"
            }
        elif code == 401:
            return {
                "status": "error",
                "message": "Token de Acesso da Meta expirado ou inválido (HTTP 401).",
                "hint": "Gere um Token Permanente no Gerenciador de Negócios da Meta."
            }
        else:
            return {
                "status": "error",
                "message": f"Falha ao validar WhatsApp Cloud API (HTTP {code}): {str(resp)[:200]}",
                "hint": "Confira se o Phone Number ID está correto."
            }

    @classmethod
    def test_whatsapp_evolution_api(
        cls,
        api_url: str,
        api_key: str,
        instance_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Testa conexão com Evolution API (Open Source local ou Docker) e lista instâncias."""
        clean_url = (api_url or "http://localhost:8080").rstrip("/")
        headers = {"apikey": api_key.strip()} if api_key else {}
        
        fetch_url = f"{clean_url}/instance/fetchInstances"
        code, resp, latency = cls._http_request(fetch_url, method="GET", headers=headers, timeout=5.0)

        if code in (200, 201) and isinstance(resp, list):
            instances = [item.get("instance", {}).get("instanceName") or item.get("name") for item in resp if isinstance(item, dict)]
            active_inst = instance_name if instance_name in instances else (instances[0] if instances else "nenhuma")
            return {
                "status": "success",
                "type": "whatsapp_evolution_opensource",
                "latency_ms": latency,
                "instances_count": len(instances),
                "instances": instances,
                "active_instance": active_inst,
                "message": f"Evolution API conectada! {len(instances)} instância(s) encontrada(s)."
            }
        elif code in (401, 403):
            return {
                "status": "error",
                "message": "Chave da Evolution API (apikey) incorreta.",
                "hint": "Verifique a chave de API nas configurações da sua Evolution API."
            }
        else:
            return {
                "status": "error",
                "message": f"Não foi possível conectar à Evolution API em {clean_url}.",
                "hint": "Se estiver rodando no Docker, verifique se o container está ativo na porta 8080."
            }

    @classmethod
    def test_meta_graph_api(
        cls,
        access_token: str
    ) -> Dict[str, Any]:
        """
        Valida o token da Meta Graph API e descobre automaticamente
        todas as páginas do Facebook e contas profissionais do Instagram conectadas!
        """
        if not access_token:
            return {
                "status": "error",
                "message": "Informe o Token de Acesso da Meta Graph API.",
                "hint": "Gere no Meta for Developers com permissões: instagram_basic, instagram_content_publish, pages_show_list."
            }

        url = "https://graph.facebook.com/v20.0/me?fields=id,name,accounts{id,name,access_token,instagram_business_account{id,username,name,profile_picture_url}}"
        headers = {"Authorization": f"Bearer {access_token.strip()}"}
        code, resp, latency = cls._http_request(url, method="GET", headers=headers, timeout=10.0)

        if code == 200 and isinstance(resp, dict):
            user_name = resp.get("name", "Usuário Meta")
            accounts_data = resp.get("accounts", {}).get("data", [])
            
            discovered_pages = []
            discovered_instagram = []

            for acc in accounts_data:
                page_info = {
                    "page_id": acc.get("id"),
                    "page_name": acc.get("name"),
                    "page_token": acc.get("access_token")
                }
                discovered_pages.append(page_info)
                
                ig_info = acc.get("instagram_business_account")
                if ig_info:
                    discovered_instagram.append({
                        "ig_id": ig_info.get("id"),
                        "username": ig_info.get("username"),
                        "name": ig_info.get("name"),
                        "avatar": ig_info.get("profile_picture_url"),
                        "linked_page_id": acc.get("id")
                    })

            return {
                "status": "success",
                "user_name": user_name,
                "latency_ms": latency,
                "pages": discovered_pages,
                "instagram_accounts": discovered_instagram,
                "message": f"Meta Graph API Conectada! Usuário: {user_name} | {len(discovered_instagram)} conta(s) do Instagram e {len(discovered_pages)} página(s) encontradas."
            }
        elif code == 401:
            return {
                "status": "error",
                "message": "Token de Acesso da Meta expirado ou inválido (HTTP 401).",
                "hint": "Gere um Token de Usuário do Sistema de Longa Duração."
            }
        else:
            return {
                "status": "error",
                "message": f"Erro na consulta à Meta Graph API (HTTP {code}): {str(resp)[:200]}",
                "hint": "Confira as permissões do aplicativo no painel da Meta."
            }

    @classmethod
    def test_telegram_bot(
        cls,
        bot_token: str,
        chat_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Testa o token do Bot do Telegram usando /getMe."""
        if not bot_token:
            return {"status": "error", "message": "Informe o Token do Bot do Telegram."}

        url = f"https://api.telegram.org/bot{bot_token.strip()}/getMe"
        code, resp, latency = cls._http_request(url, method="GET", timeout=8.0)

        if code == 200 and isinstance(resp, dict) and resp.get("ok"):
            bot_info = resp.get("result", {})
            return {
                "status": "success",
                "latency_ms": latency,
                "bot_username": f"@{bot_info.get('username')}",
                "bot_name": bot_info.get("first_name"),
                "message": f"Bot do Telegram conectado: @{bot_info.get('username')} ({bot_info.get('first_name')})"
            }
        else:
            return {
                "status": "error",
                "message": "Token do Bot do Telegram inválido.",
                "hint": "Obtenha seu token conversando com o @BotFather no Telegram."
            }

    @staticmethod
    def detect_local_hardware() -> Dict[str, Any]:
        """
        Inspeciona a máquina do usuário para identificar se é um PC Leve (CPU/RAM modesta)
        ou um PC Potente (NVIDIA RTX com VRAM suficiente).
        """
        info = {
            "os": platform.system(),
            "os_release": platform.release(),
            "processor": platform.processor(),
            "has_nvidia_gpu": False,
            "gpu_name": "Nenhuma detectada",
            "vram_gb": 0.0,
            "profile": "light",
            "recommendation": ""
        }

        try:
            cmd = "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
            if res.returncode == 0 and res.stdout.strip():
                lines = res.stdout.strip().split("\n")
                if lines:
                    first = lines[0].split(",")
                    info["has_nvidia_gpu"] = True
                    info["gpu_name"] = first[0].strip()
                    if len(first) > 1:
                        try:
                            vram_mb = float(first[1].strip())
                            info["vram_gb"] = round(vram_mb / 1024.0, 1)
                        except Exception:
                            pass
        except Exception:
            pass

        if info["has_nvidia_gpu"] and info["vram_gb"] >= 6.0:
            info["profile"] = "heavy"
            info["recommendation"] = f"PC Potente detectado ({info['gpu_name']} com {info['vram_gb']}GB VRAM). Você pode usar Ollama local com máxima velocidade e renderizar vídeos na sua própria máquina!"
        elif info["has_nvidia_gpu"] and info["vram_gb"] >= 4.0:
            info["profile"] = "medium"
            info["recommendation"] = f"PC Médio detectado ({info['gpu_name']} com {info['vram_gb']}GB VRAM). Recomendamos Ollama com modelos de 7B (como qwen2.5:7b) ou APIs em nuvem (Maritaca AI / DeepSeek)."
        else:
            info["profile"] = "light"
            info["recommendation"] = "PC Leve detectado (Sem GPU dedicada). Perfeito para usar com Maritaca AI (Sabiá-3) ou DeepSeek via API, e conectar ao Worker Colab gratuito em 1 clique para renderizar vídeos sem pesar no seu computador!"

        return info
