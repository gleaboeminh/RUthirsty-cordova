"""
Build-time helper: generate toeic_icon.ico for PyInstaller.
Requires Pillow (pip install Pillow).
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys


def make_frame(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded background: blue gradient-ish solid
    bg_color = (41, 128, 185, 255)
    r = max(size // 8, 4)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=bg_color)

    # White "T" letter, proportional to size
    w = size
    # Top horizontal bar
    bar_left  = int(w * 0.12)
    bar_right = int(w * 0.88)
    bar_top   = int(w * 0.15)
    bar_bot   = int(w * 0.35)
    draw.rectangle([bar_left, bar_top, bar_right, bar_bot], fill=(255, 255, 255, 255))

    # Vertical stem
    stem_left  = int(w * 0.40)
    stem_right = int(w * 0.60)
    stem_top   = int(w * 0.35)
    stem_bot   = int(w * 0.85)
    draw.rectangle([stem_left, stem_top, stem_right, stem_bot], fill=(255, 255, 255, 255))

    return img


def build_ico(out_path: str = "toeic_icon.ico"):
    sizes = [256, 128, 64, 48, 32, 16]
    frames = [make_frame(s) for s in sizes]
    frames[0].save(
        out_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print(f"Icon saved to: {os.path.abspath(out_path)}")


if __name__ == "__main__":
    build_ico()
