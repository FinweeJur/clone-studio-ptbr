import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from app.core.config import settings

class ThumbnailGenerator:
    """
    Gera automaticamente capas e thumbnails para vídeos verticais (Reels, TikTok, Shorts):
    - Extrai o melhor frame do vídeo (ou imagem de referência do clone).
    - Aplica o Gancho Viral em tipografia destacada com contraste otimizado.
    """

    @classmethod
    def generate_cover(
        cls,
        video_or_image_path: Path,
        hook_text: str,
        output_name: Optional[str] = None
    ) -> Path:
        """Extrai o frame e gera o arquivo de capa."""
        settings.ensure_directories()
        out_name = output_name or f"capa_{Path(video_or_image_path).stem}.jpg"
        target_path = settings.OUTPUTS_DIR / out_name

        clean_hook = hook_text.strip()
        if len(clean_hook) > 80:
            clean_hook = clean_hook[:77] + "..."

        # Se ffmpeg estiver disponível no PATH, extrai o frame e aplica legenda com filtro
        ffmpeg_bin = "ffmpeg"
        
        # 1. Tentar extrair o frame aos 1.5s
        frame_tmp = settings.OUTPUTS_DIR / f"temp_frame_{out_name}.jpg"
        
        is_video = str(video_or_image_path).lower().endswith((".mp4", ".mov", ".webm", ".mkv"))

        if is_video and Path(video_or_image_path).exists():
            extract_cmd = [
                ffmpeg_bin, "-y",
                "-ss", "00:00:01.500",
                "-i", str(video_or_image_path),
                "-vframes", "1",
                "-q:v", "2",
                str(frame_tmp)
            ]
            try:
                res = subprocess.run(extract_cmd, capture_output=True, text=True, timeout=10)
                if res.returncode == 0 and frame_tmp.exists():
                    source_img = frame_tmp
                else:
                    source_img = video_or_image_path
            except Exception:
                source_img = video_or_image_path
        else:
            source_img = video_or_image_path

        # Tentar usar PIL se instalado para desenhar texto limpo com fundo semitransparente
        try:
            from PIL import Image, ImageDraw, ImageFont
            if Path(source_img).exists():
                img = Image.open(source_img).convert("RGB")
                img = img.resize((1080, 1920))
                draw = ImageDraw.Draw(img, "RGBA")

                # Faixa escura no centro/terço superior para legibilidade
                box_top = 400
                box_height = 280
                draw.rectangle([(60, box_top), (1020, box_top + box_height)], fill=(0, 0, 0, 180))
                draw.rectangle([(60, box_top), (1020, box_top + 8)], fill=(245, 158, 11, 255)) # Borda âmbar

                # Tentar carregar fonte padrão ou usar default
                try:
                    font = ImageFont.truetype("arial.ttf", 46)
                except Exception:
                    font = ImageFont.load_default()

                # Quebra de texto simples
                words = clean_hook.split(" ")
                lines = []
                cur = ""
                for w in words:
                    if len(cur + " " + w) < 28:
                        cur += (" " if cur else "") + w
                    else:
                        lines.append(cur)
                        cur = w
                if cur:
                    lines.append(cur)

                y_offset = box_top + 30
                for line in lines[:3]:
                    draw.text((100, y_offset), line, fill=(255, 255, 255, 255), font=font)
                    y_offset += 65

                img.save(target_path, quality=92)
                if frame_tmp.exists() and frame_tmp != target_path:
                    try:
                        frame_tmp.unlink()
                    except Exception:
                        pass
                return target_path
        except Exception:
            pass

        # Fallback resiliente: copia o frame_tmp ou cria arquivo de capa básico
        if frame_tmp.exists():
            if target_path.exists():
                target_path.unlink()
            frame_tmp.rename(target_path)
            return target_path
        elif Path(source_img).exists():
            import shutil
            shutil.copyfile(source_img, target_path)
            return target_path
        else:
            # Cria marcador vazio
            with open(target_path, "wb") as f:
                f.write(b"")
            return target_path
