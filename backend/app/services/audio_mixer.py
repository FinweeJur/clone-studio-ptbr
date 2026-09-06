import subprocess
from pathlib import Path
from typing import Optional

class AudioMixer:
    """
    Serviço de mixagem de áudio com auto-ducking inteligente:
    Reduz automaticamente o volume da trilha sonora (BGM) quando o clone estiver falando.
    """

    @staticmethod
    def mix_speech_with_bgm(
        speech_audio_path: Path,
        bgm_audio_path: Path,
        output_audio_path: Path,
        bgm_base_volume: float = 0.15,
        ducking_ratio: float = 0.05
    ) -> Path:
        """
        Usa o filtro sidechaincompress do FFmpeg para fazer o auto-ducking da música quando a voz fala.
        """
        output_audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Filtro de sidechain:
        # [1:a] é o BGM, ajustado com volume inicial
        # [0:a] é a voz do narrador (controlador do sidechain)
        # Quando a voz sobe, comprime o BGM
        filter_complex = (
            f"[1:a]volume={bgm_base_volume}[bgm];"
            f"[bgm][0:a]sidechaincompress=threshold=0.03:ratio=10:attack=100:release=600[ducked_bgm];"
            f"[0:a][ducked_bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(speech_audio_path),
            "-stream_loop", "-1", "-i", str(bgm_audio_path),
            "-filter_complex", filter_complex,
            "-map", "[outa]",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_audio_path)
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            # Fallback simples caso o áudio BGM tenha canais diferentes
            simple_filter = f"[1:a]volume={bgm_base_volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[outa]"
            fallback_cmd = [
                "ffmpeg", "-y",
                "-i", str(speech_audio_path),
                "-stream_loop", "-1", "-i", str(bgm_audio_path),
                "-filter_complex", simple_filter,
                "-map", "[outa]",
                "-c:a", "aac",
                "-b:a", "192k",
                str(output_audio_path)
            ]
            subprocess.run(fallback_cmd, check=True)

        return output_audio_path
