import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.core.config import settings
from app.services.subtitle_generator import SubtitleGenerator, SubtitleStyle

def test_subtitle_smart_line_break():
    print("[*] Testando quebra inteligente de linha sem orfaos...")
    test_text = "Voce sabia que a inteligencia artificial pode aprender a sua voz em segundos?"
    broken = SubtitleGenerator.smart_line_break_ptbr(test_text, max_chars_per_line=30)
    print(f"Original: {test_text}")
    print(f"Formatado ASS: {broken}")
    assert "\\N" in broken or len(test_text) <= 30
    print("[+] Teste de quebra inteligente: PASSOU!")

def test_ass_generation():
    print("[*] Testando geracao dos 5 estilos de legenda ASS...")
    for style in [SubtitleStyle.HORMOZI, SubtitleStyle.KARAOKE, SubtitleStyle.MINIMALIST, SubtitleStyle.BOXED_DARK, SubtitleStyle.GRADIENT_NEON]:
        header = SubtitleGenerator.get_ass_header(style)
        assert "Style: Default" in header
        print(f"  - Estilo '{style}': OK")
    print("[+] Teste de estilos ASS: PASSOU!")

def test_config_paths():
    print("[*] Testando caminhos e pastas...")
    assert settings.DATA_DIR.exists()
    assert settings.CLONES_DIR.exists()
    assert settings.OUTPUTS_DIR.exists()
    print("[+] Teste de diretorios: PASSOU!")

if __name__ == "__main__":
    test_subtitle_smart_line_break()
    test_ass_generation()
    test_config_paths()
    print("\n[OK] TODOS OS TESTES PASSARAM COM SUCESSO!")
