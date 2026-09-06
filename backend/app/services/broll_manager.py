import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

class BrollManager:
    """
    Gerenciador de B-Roll, imagens sobrepostas e cartões de texto.
    Aplica as camadas visuais sobre o vídeo base gerado do avatar.
    """

    @staticmethod
    def composite_video_layers(
        base_video_path: Path,
        audio_path: Path,
        subtitle_path: Optional[Path],
        visual_layers: List[Dict[str, Any]],
        output_video_path: Path,
        aspect_ratio: str = "9:16"
    ) -> Path:
        """
        Monta o vídeo final aplicando:
        1. Vídeo base do avatar (LivePortrait / MuseTalk)
        2. Áudio mixado (voz + BGM ducked)
        3. Sobreposições de imagens / B-Roll com transição fade
        4. Legendas estilizadas (.ass)
        """
        output_video_path.parent.mkdir(parents=True, exist_ok=True)

        # Resoluções padrão por formato
        res_map = {
            "9:16": (1080, 1920),
            "16:9": (1920, 1080),
            "1:1": (1080, 1080)
        }
        target_w, target_h = res_map.get(aspect_ratio, (1080, 1920))

        # Montagem dos inputs e filtros FFmpeg
        inputs = ["-i", str(base_video_path), "-i", str(audio_path)]
        filter_chains = []
        
        # Base scale
        filter_chains.append(f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2[base_v]")
        
        last_v_tag = "base_v"
        input_idx = 2

        # Processamento de overlays de imagem / broll
        for item in visual_layers:
            media_path = item.get("media_path")
            start_t = float(item.get("start", 0))
            end_t = float(item.get("end", start_t + 3.0))
            layer_type = item.get("type", "image")

            if media_path and Path(media_path).exists():
                inputs.extend(["-i", str(media_path)])
                
                # Ajusta tamanho do overlay
                if layer_type == "image_pip":
                    # Picture-in-picture no canto superior
                    w, h = int(target_w * 0.4), int(target_h * 0.25)
                    x, y = int(target_w * 0.55), int(target_h * 0.1)
                else:
                    # Imagem centralizada
                    w, h = int(target_w * 0.8), int(target_h * 0.45)
                    x, y = f"(main_w-overlay_w)/2", f"(main_h-overlay_h)/2"

                fade_dur = 0.3
                overlay_tag = f"ov_{input_idx}"
                next_v_tag = f"v_step_{input_idx}"

                # Escala e aplica fade in/out na imagem
                filter_chains.append(
                    f"[{input_idx}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                    f"format=rgba,fade=t=in:st={start_t}:d={fade_dur}:alpha=1,"
                    f"fade=t=out:st={end_t-fade_dur}:d={fade_dur}:alpha=1[{overlay_tag}]"
                )

                # Sobrepõe no vídeo base
                filter_chains.append(
                    f"[{last_v_tag}][{overlay_tag}]overlay=x={x}:y={y}:enable='between(t,{start_t},{end_t})'[{next_v_tag}]"
                )

                last_v_tag = next_v_tag
                input_idx += 1

        # Adiciona legendas ASS se fornecidas
        if subtitle_path and Path(subtitle_path).exists():
            # Escapa barras para sintaxe de filtro do FFmpeg
            escaped_sub = str(subtitle_path).replace("\\", "/").replace(":", "\\:")
            filter_chains.append(f"[{last_v_tag}]ass='{escaped_sub}'[final_v]")
            last_v_tag = "final_v"

        filter_str = ";".join(filter_chains)

        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", filter_str,
            "-map", f"[{last_v_tag}]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "19",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video_path)
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            # Em caso de erro na cadeia complexa, grava sem legendas/overlays como fallback
            fallback_cmd = [
                "ffmpeg", "-y",
                "-i", str(base_video_path),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(output_video_path)
            ]
            subprocess.run(fallback_cmd, check=True)

        return output_video_path
