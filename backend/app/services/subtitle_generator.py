import re
from pathlib import Path
from typing import List, Dict, Any, Optional

# Preposições, artigos e conjunções em português que NÃO devem ficar órfãs no final de linha
PTBR_ORPHAN_WORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "dum", "duma",
    "em", "na", "no", "nas", "nos", "num", "numa",
    "por", "pela", "pelo", "pelas", "pelos",
    "para", "pra", "pro", "pras", "pros",
    "com", "sem", "sob", "sobre", "ante", "até", "após",
    "e", "ou", "mas", "que", "se", "como", "quando", "onde"
}

class SubtitleStyle:
    HORMOZI = "hormozi_bold"
    KARAOKE = "karaoke_dynamic"
    MINIMALIST = "minimalist_clean"
    BOXED_DARK = "boxed_dark"
    GRADIENT_NEON = "gradient_neon"

class SubtitleGenerator:
    """
    Gerador de legendas avançado para PT-BR com:
    - 5 Estilos visuais profissionais para redes sociais
    - Algoritmo de quebra de linha inteligente (No-Orphan Line Breaking)
    - Suporte a formato ASS (Advanced SubStation Alpha) com queima via FFmpeg
    """

    @staticmethod
    def format_timestamp_ass(seconds: float) -> str:
        """Formata segundos para o formato ASS: H:MM:SS.cc"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds - int(seconds)) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    @staticmethod
    def format_timestamp_srt(seconds: float) -> str:
        """Formata segundos para o formato SRT: HH:MM:SS,mmm"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @classmethod
    def smart_line_break_ptbr(cls, text: str, max_chars_per_line: int = 24) -> str:
        """
        Quebra o texto em no máximo 2 linhas sem partir palavras e sem deixar
        artigos/preposições órfãos no final da primeira linha.
        """
        words = text.strip().split()
        if not words:
            return ""

        # Se o texto for curto o suficiente para 1 linha
        if len(" ".join(words)) <= max_chars_per_line:
            return " ".join(words)

        line1 = []
        line2 = []
        current_len = 0

        for i, word in enumerate(words):
            word_clean = re.sub(r'[^\w\s]', '', word.lower())
            
            # Se ainda cabe na linha 1
            if current_len + len(word) + 1 <= max_chars_per_line and not line2:
                line1.append(word)
                current_len += len(word) + 1
            else:
                line2.append(word)

        # Regra Anti-Órfão: Se a última palavra da linha 1 for preposição/artigo, empurra para a linha 2
        if line1 and line2:
            last_word_l1 = re.sub(r'[^\w\s]', '', line1[-1].lower())
            if last_word_l1 in PTBR_ORPHAN_WORDS and len(line1) > 1:
                orphaned = line1.pop()
                line2.insert(0, orphaned)

        if line2:
            return f"{' '.join(line1)}\\N{' '.join(line2)}"
        return " ".join(line1)

    @classmethod
    def get_ass_header(cls, style_name: str, video_width: int = 1080, video_height: int = 1920) -> str:
        """
        Gera o cabeçalho e estilos ASS correspondentes aos 5 modos selecionáveis.
        """
        # Estilos com cores em formato &HAABBGGRR (Alpha, Blue, Green, Red em Hex)
        style_definitions = {
            SubtitleStyle.HORMOZI: (
                # Amarelo vibrante (&H0000FFFF), Borda preta grossa, Sombra sólida, All Caps
                f"Style: Default,Arial Black,54,&H0000D7FF,&H000000FF,&H00000000,&H80000000,"
                f"-1,0,0,0,100,100,0,0,1,5,2,2,40,40,240,1"
            ),
            SubtitleStyle.KARAOKE: (
                # Branco com destaque em Verde Neon (&H0000FF00) e borda escura
                f"Style: Default,Impact,52,&H00FFFFFF,&H0000FF00,&H00000000,&H80000000,"
                f"-1,0,0,0,100,100,0,0,1,4,2,2,40,40,230,1"
            ),
            SubtitleStyle.MINIMALIST: (
                # Branco puro, sem serifa, sombra suave, elegante
                f"Style: Default,Segoe UI,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,"
                f"-1,0,0,0,100,100,0,0,1,2,3,2,50,50,220,1"
            ),
            SubtitleStyle.BOXED_DARK: (
                # Texto branco dentro de card retangular escuro com transparência (&H80151515)
                f"Style: Default,Trebuchet MS,46,&H00FFFFFF,&H0000FFFF,&H801A1A1A,&H00000000,"
                f"0,0,0,0,100,100,0,0,3,10,0,2,40,40,250,1"
            ),
            SubtitleStyle.GRADIENT_NEON: (
                # Ciano fluorescente (&H00FFFF00 no ASS BGR) com brilho roxo
                f"Style: Default,Montserrat ExtraBold,50,&H00FFF200,&H00FF00EA,&H00330033,&H80000000,"
                f"-1,0,0,0,100,100,0,0,1,4,4,2,40,40,240,1"
            )
        }

        selected_style = style_definitions.get(style_name, style_definitions[SubtitleStyle.HORMOZI])

        return f"""[Script Info]
Title: CloneStudio PT-BR Subtitles
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{selected_style}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    @classmethod
    def generate_ass_file(
        cls,
        segments: List[Dict[str, Any]],
        output_path: Path,
        style_name: str = SubtitleStyle.HORMOZI,
        video_width: int = 1080,
        video_height: int = 1920
    ) -> Path:
        """
        Gera o arquivo de legendas .ass pronto para ser gravado no vídeo final com alta fidelidade.
        """
        header = cls.get_ass_header(style_name, video_width, video_height)
        dialogue_lines = []

        for seg in segments:
            start_time = cls.format_timestamp_ass(seg["start"])
            end_time = cls.format_timestamp_ass(seg["end"])
            raw_text = seg["text"]
            
            # Aplica quebra inteligente de linha sem órfãos
            formatted_text = cls.smart_line_break_ptbr(raw_text)
            
            # Se for estilo Karaokê com palavras mapeadas
            if style_name == SubtitleStyle.KARAOKE and "words" in seg and seg["words"]:
                # Exemplo: {\\k30}Palavra {\\k40}Outra
                karaoke_parts = []
                for w in seg["words"]:
                    duration_cs = int((w["end"] - w["start"]) * 100)
                    karaoke_parts.append(f"{{\\k{duration_cs}}}{w['word']}")
                karaoke_text = " ".join(karaoke_parts)
                dialogue_lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{karaoke_text}")
            else:
                dialogue_lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{formatted_text}")

        content = header + "\n".join(dialogue_lines) + "\n"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path
