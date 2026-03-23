#!/usr/bin/env python3
"""
Generate screenshots for README.
Run: python _make_screenshots.py
Produces: screenshots/context_menu.png, screenshots/progress.png, screenshots/settings.png
"""
import os, sys, time, threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

OUT = Path(__file__).parent / "screenshots"
OUT.mkdir(exist_ok=True)


# ── 1. Mock context menu screenshot ──────────────────────────────────────────
def make_context_menu():
    from PIL import Image, ImageDraw, ImageFont

    W, H = 520, 380

    def font(size, bold=False):
        candidates = (
            [f"C:/Windows/Fonts/segoeuib.ttf"] if bold else []
        ) + ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
        for p in candidates:
            try: return ImageFont.truetype(p, size)
            except: pass
        return ImageFont.load_default()

    img  = Image.new("RGB", (W, H), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    # Desktop background
    img.paste((30, 100, 180), (0, 0, W, H))
    # File icon area
    draw.rectangle([30, 60, 490, 320], fill=(255, 255, 255), outline=(180, 180, 180))

    # Simulate file in explorer
    FN = font(11)
    FB = font(11, bold=True)

    # Explorer-style header
    draw.rectangle([30, 60, 490, 85], fill=(243, 243, 243))
    draw.text((40, 67), "Documents", font=FN, fill=(0, 0, 0))

    # File rows
    items = [
        ("📄 report.txt",           "2 KB",  "Text Document", True),
        ("📝 contract.docx",        "18 KB", "Word Document",  False),
        ("📕 user_manual.pdf",      "340 KB","PDF Document",   False),
    ]
    for i, (name, size, kind, selected) in enumerate(items):
        y = 100 + i * 26
        bg = (204, 232, 255) if selected else (255, 255, 255)
        draw.rectangle([31, y, 489, y + 25], fill=bg)
        draw.text((50, y + 5), name,  font=FB if selected else FN, fill=(0, 0, 0))
        draw.text((340, y + 5), size, font=FN, fill=(80, 80, 80))
        draw.text((400, y + 5), kind, font=FN, fill=(80, 80, 80))

    # Context menu
    MX, MY, MW = 220, 110, 240
    MENU_ITEMS = [
        ("Open",                     False, False),
        ("Open with",                False, False),
        (None,                       False, True),   # separator
        ("Cut",                      False, False),
        ("Copy",                     False, False),
        (None,                       False, True),
        ("Translate with TinyTranslate", True, False),
        (None,                       False, True),
        ("Properties",               False, False),
    ]
    MH = sum(24 if not sep else 9 for _, _, sep in MENU_ITEMS) + 8
    draw.rectangle([MX, MY, MX + MW, MY + MH], fill=(249, 249, 249),
                   outline=(180, 180, 180))
    cy = MY + 4
    icon_path = Path(__file__).parent / "assets" / "icon.ico"
    icon_img = None
    try:
        icon_img = Image.open(icon_path).resize((16, 16), Image.LANCZOS).convert("RGBA")
    except: pass

    for label, highlight, sep in MENU_ITEMS:
        if sep:
            draw.line([MX + 6, cy + 4, MX + MW - 6, cy + 4], fill=(210, 210, 210))
            cy += 9
        else:
            if highlight:
                draw.rectangle([MX + 1, cy, MX + MW - 1, cy + 23],
                                fill=(0, 120, 215))
                color = (255, 255, 255)
                if icon_img:
                    img.paste(icon_img, (MX + 6, cy + 3), icon_img)
                draw.text((MX + 26 if icon_img else MX + 10, cy + 4),
                          label, font=font(11, True), fill=color)
            else:
                draw.text((MX + 10, cy + 4), label, font=FN, fill=(0, 0, 0))
            cy += 24

    # Drop shadow
    shadow = Image.new("RGB", (W + 6, H + 6), (200, 200, 200))
    shadow.paste(img, (3, 3))
    shadow.paste(img, (0, 0))
    shadow.save(OUT / "context_menu.png")
    print(f"[OK] {OUT / 'context_menu.png'}")


# ── 2. Progress window screenshot ────────────────────────────────────────────
def make_progress():
    import tkinter as tk
    from PIL import ImageGrab

    done = threading.Event()
    path = OUT / "progress.png"

    def _run():
        BG, ACCENT, SUBTEXT = "#1e1e2e", "#89b4fa", "#a6adc8"
        root = tk.Tk()
        root.title("TinyTranslate")
        root.geometry("380x100")
        root.resizable(False, False)
        root.configure(bg=BG)
        root.eval("tk::PlaceWindow . center")

        tk.Label(root, text="TinyTranslate", bg=BG, fg=ACCENT,
                 font=("Segoe UI", 12, "bold")).pack(pady=(16, 3))
        tk.Label(root, text="Translating EN → FR  (2/4)",
                 bg=BG, fg=SUBTEXT, font=("Segoe UI", 9)).pack()

        def _shot():
            root.update()
            x, y = root.winfo_rootx(), root.winfo_rooty()
            w, h = root.winfo_width(), root.winfo_height()
            img = ImageGrab.grab((x - 1, y - 1, x + w + 1, y + h + 1))
            img.save(path)
            print(f"[OK] {path}")
            root.after(100, root.destroy)
            done.set()

        root.after(600, _shot)
        root.mainloop()

    t = threading.Thread(target=_run)
    t.start()
    done.wait(timeout=8)


# ── 3. Settings window screenshot — uses the real settings.py ────────────────
def make_settings():
    import tkinter as tk
    from tkinter import ttk
    from PIL import ImageGrab
    import types

    done = threading.Event()
    path = OUT / "settings.png"

    # Patch config + translator so settings.py runs without real installs
    import config as _real_cfg
    sys.modules.pop("config", None)
    fake_cfg = types.ModuleType("config")
    fake_cfg.VERSION     = _real_cfg.VERSION
    fake_cfg.LANGUAGES   = _real_cfg.LANGUAGES
    fake_cfg.load_config = lambda: {"source_lang": "en", "target_lang": "fr", "chunk_size": 1500}
    fake_cfg.save_config = lambda c: None
    fake_cfg.CONFIG_PATH = ""
    sys.modules["config"] = fake_cfg

    sys.modules.pop("core.translator", None)
    fake_trans = types.ModuleType("core.translator")
    fake_trans.list_installed_pairs = lambda: [("en", "fr"), ("en", "he"), ("en", "es")]
    fake_trans.install_language_pack = lambda f, t: None
    fake_trans.is_pack_installed = lambda f, t: (f, t) in [("en", "fr"), ("en", "he"), ("en", "es")]
    sys.modules["core.translator"] = fake_trans

    sys.modules.pop("core.registry", None)
    fake_reg = types.ModuleType("core.registry")
    fake_reg.register = lambda src="en": 3
    sys.modules["core.registry"] = fake_reg

    # Import actual settings module fresh
    sys.modules.pop("settings", None)
    import importlib, settings as stg
    importlib.reload(stg)

    def _run():
        # Monkey-patch mainloop to auto-screenshot and quit
        original_mainloop = tk.Tk.mainloop

        call_count = [0]
        def patched_mainloop(self, *args, **kwargs):
            call_count[0] += 1
            if call_count[0] > 1:
                return
            def _shot():
                self.update()
                x, y = self.winfo_rootx(), self.winfo_rooty()
                w, h = self.winfo_width(), self.winfo_height()
                ImageGrab.grab((x-1, y-1, x+w+1, y+h+1)).save(path)
                print(f"[OK] {path}")
                self.after(100, self.destroy)
                done.set()
            self.after(800, _shot)
            original_mainloop(self, *args, **kwargs)

        tk.Tk.mainloop = patched_mainloop
        try:
            stg.main()
        finally:
            tk.Tk.mainloop = original_mainloop

    t = threading.Thread(target=_run)
    t.start()
    done.wait(timeout=10)


if __name__ == "__main__":
    print("Generating screenshots...")
    make_context_menu()
    make_progress()
    make_settings()
    print("\nAll screenshots saved to screenshots/")
