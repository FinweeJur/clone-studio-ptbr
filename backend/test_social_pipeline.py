import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.social_publishers.whatsapp_publisher import WhatsAppPublisher
from app.api.endpoints_social import load_social_config, save_social_config

def test_deep_links():
    print("[*] Testando geracao de links rapidos de compartilhamento...")
    caption = "Confira meu novo video com IA! #tech"
    wa_link = WhatsAppPublisher.generate_whatsapp_deep_link(caption)
    assert "api.whatsapp.com/send" in wa_link
    assert "Confira" in wa_link
    print(f"  - WhatsApp Link: {wa_link[:60]}... OK")

def test_social_config():
    print("[*] Testando persistencia de configuracoes de redes...")
    cfg = load_social_config()
    assert isinstance(cfg, dict)
    cfg["test_key"] = "test_val"
    save_social_config(cfg)
    reloaded = load_social_config()
    assert reloaded.get("test_key") == "test_val"
    print("  - Persistencia de credenciais: OK")

if __name__ == "__main__":
    test_deep_links()
    test_social_config()
    print("\n[OK] TODOS OS TESTES SOCIAIS PASSARAM COM SUCESSO!")
