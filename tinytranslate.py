#!/usr/bin/env python3
"""
TinyTranslate v1.0.0
Right-click any .txt, .docx, or .pdf → translate offline → save as filename_FR.txt
No API key. No cloud. Uses Argos Translate local models.
"""
import sys
import os
import threading
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, VERSION
from core.reader import read_file
from core.translator import translate, is_pack_installed, install_language_pack
from core.gui import ProgressWindow, alert


def main():
    if len(sys.argv) < 2:
        alert("error", "TinyTranslate", "Usage: tinytranslate.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1].strip('"').strip("'")
    # Optional: target language passed directly from context menu (overrides config)
    lang_override = sys.argv[2].strip('"').strip("'") if len(sys.argv) >= 3 else None

    if not os.path.isfile(file_path):
        alert("error", "TinyTranslate", f"File not found:\n{file_path}")
        sys.exit(1)

    ext = Path(file_path).suffix.lower()
    if ext not in (".txt", ".docx", ".pdf"):
        alert(
            "error", "TinyTranslate",
            f"Unsupported file type: {ext}\nSupported: .txt  .docx  .pdf",
        )
        sys.exit(1)

    cfg = load_config()
    if lang_override:
        cfg["target_lang"] = lang_override
    filename = Path(file_path).name
    progress = ProgressWindow(filename)
    result: dict = {}

    def _run():
        try:
            progress.update(f"Reading {filename}...")
            text = read_file(file_path)

            if not text.strip():
                raise ValueError("File is empty or contains no extractable text.")

            src = cfg["source_lang"]
            tgt = cfg["target_lang"]

            def _on_progress(i, total):
                suffix = f"  ({i}/{total})" if total > 1 else ""
                progress.update(f"Translating {src.upper()} → {tgt.upper()}{suffix}")

            if not is_pack_installed(src, tgt):
                progress.update(f"Downloading {src.upper()} -> {tgt.upper()} model (~100 MB)...")
                install_language_pack(src, tgt)

            progress.update(f"Translating {src.upper()} -> {tgt.upper()}...")
            translated = translate(text, src, tgt, cfg["chunk_size"], _on_progress)

            out_path = _output_path(file_path, tgt)
            progress.update(f"Saving {Path(out_path).name}...")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(translated)

            result["output"] = out_path

        except Exception as e:
            result["error"] = str(e)
            _write_log(file_path, e)
        finally:
            progress.root.after(0, progress.close)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    progress.root.mainloop()
    t.join()

    if "error" in result:
        alert("error", "TinyTranslate", result["error"])
        sys.exit(1)

    out_name = Path(result["output"]).name
    alert("info", "TinyTranslate", f"Done!\n\nSaved as:  {out_name}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _output_path(input_path: str, target_lang: str) -> str:
    p = Path(input_path)
    return str(p.parent / f"{p.stem}_{target_lang.upper()}.txt")


def _write_log(file_path: str, exc: Exception):
    try:
        import traceback, datetime
        log = Path(__file__).parent / "error.log"
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.datetime.now()}] {file_path}\n")
            f.write(traceback.format_exc())
            f.write("\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
