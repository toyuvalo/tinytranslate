#!/usr/bin/env python3
"""
Generate TinyTranslate icon — assets/icon.ico
Run: python make_icon.py
Requires: Pillow
"""
import os
from pathlib import Path


def _rounded_rect(draw, bbox, radius, fill):
    x1, y1, x2, y2 = bbox
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2 * radius, y1 + 2 * radius], fill=fill)
    draw.ellipse([x2 - 2 * radius, y1, x2, y1 + 2 * radius], fill=fill)
    draw.ellipse([x1, y2 - 2 * radius, x1 + 2 * radius, y2], fill=fill)
    draw.ellipse([x2 - 2 * radius, y2 - 2 * radius, x2, y2], fill=fill)


def _get_font(size):
    from PIL import ImageFont
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _get_font_regular(size):
    from PIL import ImageFont
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def make_icon():
    from PIL import Image, ImageDraw

    SIZES = [256, 128, 64, 48, 32, 16]
    images = []

    # Colours
    BG_COLOR   = (21, 101, 192, 255)   # #1565C0  deep blue
    TEXT_COLOR = (255, 255, 255, 255)  # white
    GOLD_COLOR = (253, 216, 53, 255)   # #FDD835  gold arrow

    for size in SIZES:
        img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        pad    = max(1, size // 16)
        radius = max(2, size // 6)
        _rounded_rect(draw, (pad, pad, size - pad - 1, size - pad - 1), radius, BG_COLOR)

        if size >= 48:
            # "T" large, centred top-half
            main_size  = max(10, int(size * 0.42))
            arrow_size = max(6,  int(size * 0.18))
            font_main  = _get_font(main_size)
            font_arrow = _get_font_regular(arrow_size)

            # Big "T"
            bb = draw.textbbox((0, 0), "T", font=font_main)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            tx = (size - tw) // 2 - bb[0]
            ty = int(size * 0.10)
            draw.text((tx, ty), "T", font=font_main, fill=TEXT_COLOR)

            # Gold arrow "→" below the T
            ab = draw.textbbox((0, 0), "→", font=font_arrow)
            aw = ab[2] - ab[0]
            ax = (size - aw) // 2 - ab[0]
            ay = ty + th + max(2, size // 20)
            draw.text((ax, ay), "→", font=font_arrow, fill=GOLD_COLOR)

            # Small "t" to the right of arrow, suggesting target language
            sb = draw.textbbox((0, 0), "t", font=font_arrow)
            sx = ax + aw + max(1, size // 24)
            sy = ay + (ab[3] - ab[1] - (sb[3] - sb[1])) // 2
            draw.text((sx, sy), "t", font=font_arrow, fill=(200, 220, 255, 200))

        elif size >= 16:
            # Tiny sizes: just "T" centred
            font = _get_font(max(6, int(size * 0.55)))
            bb = draw.textbbox((0, 0), "T", font=font)
            tx = (size - (bb[2] - bb[0])) // 2 - bb[0]
            ty = (size - (bb[3] - bb[1])) // 2 - bb[1]
            draw.text((tx, ty), "T", font=font, fill=TEXT_COLOR)

        images.append(img)

    out_dir = Path(__file__).parent / "assets"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "icon.ico"

    images[0].save(
        out_path,
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=images[1:],
    )
    print(f"[OK] Icon saved: {out_path}")
    return str(out_path)


if __name__ == "__main__":
    make_icon()
