import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.trend_radar.niche_presets import NicheManager, REGIONS_BRAZIL
from app.services.trend_radar.algorithm_knowledge import AlgorithmIntelligenceEngine
from app.services.trend_radar.video_reverse_engineer import VideoReverseEngineer

def test_niches_and_top_profiles():
    print("[*] Testando catalogo de nichos e Top 10 perfis mais bombantes...")
    niches = NicheManager.get_all_niches()
    assert len(niches) >= 7
    niche_ids = [n["id"] for n in niches]
    assert "advocacia" in niche_ids
    assert "politica" in niche_ids
    assert "tecnologia" in niche_ids
    assert "educacao" in niche_ids
    assert "publicidade" in niche_ids
    print(f"  - Nichos pre-carregados: {len(niches)} encontrados OK")

    # Test top 10 profiles for advocacia
    adv_profiles = NicheManager.get_top_profiles_for_niche("advocacia")
    assert len(adv_profiles) == 10
    assert adv_profiles[0]["username"] == "@doutortrabalhista"
    print(f"  - Top 10 Advogados Mais Bombantes: {len(adv_profiles)} perfis com metricas OK")

    # Test custom niche creation
    custom = NicheManager.create_custom_niche("Odontologia Estetica")
    assert custom["id"] == "custom_odontologia_estetica"
    assert len(custom["top_profiles"]) == 10
    print("  - Criacao de Nicho Customizado com Top 10: OK")

def test_algorithm_intelligence_and_audit():
    print("[*] Testando base algoritmica e calculador de Retention Score...")
    insights = AlgorithmIntelligenceEngine.get_official_insights()
    assert len(insights) >= 4
    pillars = AlgorithmIntelligenceEngine.get_psychological_pillars()
    assert len(pillars) == 5
    print("  - Diretrizes oficiais (Meta/Mosseri, TikTok, Shorts, Kwai): OK")
    print("  - Os 5 Gatilhos Psicologicos de Retencao: OK")

    sample_script = (
        "Voce sabia que o seu chefe nunca pode te obrigar a assinar aviso previo retroativo? "
        "A lei garante que voce tem 10 dias para receber a rescisao integral com multa. "
        "Salve esse video e compartilhe com os colegas de trabalho!"
    )
    audit = AlgorithmIntelligenceEngine.audit_script(sample_script)
    assert "retention_score" in audit
    assert audit["retention_score"] >= 60
    assert len(audit["passed_checks"]) >= 2
    print(f"  - Score Algoritmico calculado: {audit['retention_score']}/100 OK")

def test_video_reverse_engineering():
    print("[*] Testando desconstrucao de video em 4 Atos...")
    transcript = (
        "Se o seu chefe te disse isso hoje, voce tem direito a receber tudo em dobro! "
        "Primeiro: nenhuma empresa pode exigir aviso previo com data falsa. "
        "Segundo: atrasou o pagamento, cabe a multa do artigo 477 da CLT! "
        "E o motivo disso acontecer e exatamente porque voce nao conhecia a lei trabalhista."
    )
    breakdown = VideoReverseEngineer.decompose_structure(transcript, duration_sec=35.0)
    assert "hook_act" in breakdown
    assert "retain_act" in breakdown
    assert "aha_moment_act" in breakdown
    assert "loop_and_cta_act" in breakdown
    assert "pacing_analysis" in breakdown
    print(f"  - Gancho identificado: '{breakdown['hook_act']['content'][:40]}...' OK")
    print(f"  - Analise de ritmo: {breakdown['pacing_analysis']['verdict']} OK")

if __name__ == "__main__":
    test_niches_and_top_profiles()
    test_algorithm_intelligence_and_audit()
    test_video_reverse_engineering()
    print("\n[OK] TODOS OS TESTES DO RADAR E ENGENHARIA REVERSA PASSARAM COM SUCESSO!")
