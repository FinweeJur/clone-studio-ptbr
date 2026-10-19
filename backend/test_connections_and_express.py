import sys
import asyncio
from pathlib import Path

# Adiciona o diretório backend ao sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.connection_tester import ConnectionTester
from app.services.thumbnail_generator import ThumbnailGenerator
from app.api.endpoints_express import create_auto_video, ExpressVideoRequest

async def run_tests():
    print("[*] 1. Testando deteccao automatica de hardware...")
    hw = ConnectionTester.detect_local_hardware()
    assert "profile" in hw, "Profile ausente no hardware"
    assert "recommendation" in hw, "Recomendacao ausente no hardware"
    print(f"  - Perfil detectado: {hw['profile']} ({hw.get('gpu_name', 'CPU')}) - OK")

    print("[*] 2. Testando verificador de LLMs (DeepSeek, Maritaca AI e Ollama)...")
    # Testa Ollama (se nao estiver rodando, deve retornar mensagem amigavel e status error com hint)
    ollama_res = ConnectionTester.test_llm_connection("ollama")
    assert "status" in ollama_res, "Status ausente no teste do Ollama"
    print(f"  - Resposta do Ollama: {ollama_res['status']} ({ollama_res.get('message', '')[:60]}...) - OK")

    # Testa DeepSeek sem chave (deve retornar erro amigavel pedindo chave)
    ds_res = ConnectionTester.test_llm_connection("deepseek", api_key="")
    assert ds_res["status"] == "error", "DeepSeek sem chave deveria retornar erro"
    print("  - Validacao de chave ausente do DeepSeek: OK")

    # Testa Maritaca sem chave
    maritaca_res = ConnectionTester.test_llm_connection("maritaca", api_key="")
    assert maritaca_res["status"] == "error", "Maritaca sem chave deveria retornar erro"
    print("  - Validacao de chave ausente da Maritaca: OK")

    print("[*] 3. Testando verificador de WhatsApp (Cloud API e Evolution API)...")
    wa_cloud_res = ConnectionTester.test_whatsapp_cloud_api("", "")
    assert wa_cloud_res["status"] == "error", "WhatsApp Cloud sem credenciais deveria retornar erro"
    print("  - Validacao de parametros WhatsApp Cloud: OK")

    wa_evo_res = ConnectionTester.test_whatsapp_evolution_api("http://localhost:9999", "fake-key")
    assert wa_evo_res["status"] == "error", "Evolution API offline deveria falhar graciosamente"
    print("  - Fallback gracioso Evolution API: OK")

    print("[*] 4. Testando verificador de Meta Graph API...")
    meta_res = ConnectionTester.test_meta_graph_api("")
    assert meta_res["status"] == "error", "Meta Graph sem token deveria retornar erro"
    print("  - Validacao de token da Meta: OK")

    print("[*] 5. Testando gerador de Thumbnail e Capa Vertical 9:16...")
    # Cria uma imagem de teste temporaria
    dummy_img = backend_dir / "app" / "assets" / "test_ref.png"
    dummy_img.parent.mkdir(parents=True, exist_ok=True)
    if not dummy_img.exists():
        with open(dummy_img, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

    cover_path = ThumbnailGenerator.generate_cover(
        video_or_image_path=dummy_img,
        hook_text="Se o patrão te disser isso, você tem direito a receber tudo!",
        output_name="test_cover_output.jpg"
    )
    assert cover_path.exists(), "Capa gerada nao existe"
    print(f"  - Capa 9:16 gerada com sucesso em: {cover_path.name} - OK")

    print("[*] 6. Testando Modo Piloto Automatico 1-Clique (/api/express/create-auto-video)...")
    req = ExpressVideoRequest(
        niche="advocacia",
        topic="Direito a estabilidade provisoria",
        hook_text="Voce sabia que nao pode ser demitido nestes 3 casos?",
        target_platforms=["instagram", "whatsapp", "tiktok"]
    )
    result = await create_auto_video(req)
    assert result["status"] == "success", "Piloto automatico falhou"
    assert len(result["acts"]) == 4, "Deveria ter 4 atos"
    assert "instagram" in result["copies"], "Copy do Instagram ausente"
    assert "whatsapp" in result["copies"], "Copy do WhatsApp ausente"
    assert "quick_share" in result, "Links rapidos ausentes"
    score_val = result['audit'].get('retention_score', result['audit'].get('score', 0))
    print(f"  - Roteiro em 4 Atos gerado com Score {score_val}/100: OK")
    print(f"  - Copys para Instagram e WhatsApp geradas: OK")
    print(f"  - Links de 1-Clique gerados: OK")

    print("\n[OK] TODOS OS TESTES DE CONEXOES E PILOTO AUTOMATICO PASSARAM COM SUCESSO!")


if __name__ == "__main__":
    asyncio.run(run_tests())
