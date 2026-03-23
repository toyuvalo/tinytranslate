#!/usr/bin/env python3
"""
TinyTranslate Settings
Launched via desktop / start menu shortcut.
"""
import sys
import os
import threading
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import load_config, save_config, VERSION, LANGUAGES as _LANG_MAP

# ── Theme ─────────────────────────────────────────────────────────────────────
BG      = "#1e1e2e"
SURFACE = "#313244"
ACCENT  = "#89b4fa"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
GOLD    = "#f9e2af"

# Build sorted display lists from single source of truth in config.py
BY_CODE = _LANG_MAP                                      # code -> name
BY_NAME = {v: k for k, v in _LANG_MAP.items()}          # name -> code
NAMES   = sorted(_LANG_MAP.values())                     # sorted full names for combobox


def main():
    cfg  = load_config()
    root = tk.Tk()
    root.title(f"TinyTranslate  v{VERSION}  — Settings")
    root.geometry("480x380")
    root.resizable(False, False)
    root.configure(bg=BG)
    root.eval("tk::PlaceWindow . center")

    # ── Header ────────────────────────────────────────────────────────────────
    tk.Label(root, text="TinyTranslate", bg=BG, fg=ACCENT,
             font=("Segoe UI", 16, "bold")).pack(pady=(20, 2))
    tk.Label(root, text=f"v{VERSION}  ·  Offline translation, right from Explorer",
             bg=BG, fg=SUBTEXT, font=("Segoe UI", 9)).pack()

    ttk.Separator(root).pack(fill="x", padx=20, pady=12)

    # ── Language fields ───────────────────────────────────────────────────────
    frm = tk.Frame(root, bg=BG)
    frm.pack(padx=36, fill="x")

    src_var = tk.StringVar(value=BY_CODE.get(cfg.get("source_lang", "en"), "English"))
    tgt_var = tk.StringVar(value=BY_CODE.get(cfg.get("target_lang", "fr"), "French"))

    def _lang_row(parent, label, var):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=6)
        tk.Label(row, text=label, bg=BG, fg=TEXT,
                 font=("Segoe UI", 10), width=18, anchor="w").pack(side="left")
        cb = ttk.Combobox(row, textvariable=var, values=NAMES,
                          state="readonly", width=22, font=("Segoe UI", 10))
        cb.pack(side="left")
        return cb

    src_cb = _lang_row(frm, "Source language", src_var)
    tgt_cb = _lang_row(frm, "Target language", tgt_var)

    # ── Pack status + download button ─────────────────────────────────────────
    status_row = tk.Frame(root, bg=BG)
    status_row.pack(padx=36, fill="x", pady=(2, 0))

    status_lbl = tk.Label(status_row, text="", bg=BG,
                          font=("Segoe UI", 9), anchor="w")
    status_lbl.pack(side="left", fill="x", expand=True)

    dl_btn = tk.Button(status_row, text="Download pack",
                       bg=GOLD, fg="#1e1e2e", font=("Segoe UI", 9, "bold"),
                       relief="flat", padx=12, pady=3, cursor="hand2")

    def _update_status(*_):
        src_code = BY_NAME.get(src_var.get())
        tgt_code = BY_NAME.get(tgt_var.get())
        if not src_code or not tgt_code:
            return
        try:
            from core.translator import is_pack_installed
            installed = is_pack_installed(src_code, tgt_code)
        except Exception:
            installed = False

        if installed:
            dl_btn.pack_forget()
            status_lbl.config(
                text=f"✓  {src_var.get()} → {tgt_var.get()} is ready",
                fg=GREEN,
            )
        else:
            status_lbl.config(
                text=f"  {src_var.get()} → {tgt_var.get()} not downloaded",
                fg=SUBTEXT,
            )
            dl_btn.pack(side="right")

    src_cb.bind("<<ComboboxSelected>>", _update_status)
    tgt_cb.bind("<<ComboboxSelected>>", _update_status)

    def _do_download():
        src_code = BY_NAME.get(src_var.get())
        tgt_code = BY_NAME.get(tgt_var.get())
        dl_btn.config(state="disabled")
        status_lbl.config(
            text=f"  Downloading {src_var.get()} → {tgt_var.get()} (~100 MB)…",
            fg=GOLD,
        )
        root.update()

        def _worker():
            try:
                from core.translator import install_language_pack
                from core.registry import register
                install_language_pack(src_code, tgt_code)
                register(src_code)   # rebuild context menu with the new language
                root.after(0, _update_status)
            except Exception as e:
                root.after(0, lambda: status_lbl.config(
                    text=f"  Error: {e}", fg=RED))
            finally:
                root.after(0, lambda: dl_btn.config(state="normal"))

        threading.Thread(target=_worker, daemon=True).start()

    dl_btn.config(command=_do_download)
    _update_status()   # set initial state

    # ── Chunk size ────────────────────────────────────────────────────────────
    ttk.Separator(root).pack(fill="x", padx=20, pady=12)

    chunk_row = tk.Frame(root, bg=BG)
    chunk_row.pack(padx=36, fill="x")
    tk.Label(chunk_row, text="Chunk size (chars)", bg=BG, fg=TEXT,
             font=("Segoe UI", 10), width=18, anchor="w").pack(side="left")
    chunk_var = tk.IntVar(value=cfg.get("chunk_size", 1500))
    tk.Spinbox(chunk_row, from_=200, to=5000, increment=100,
               textvariable=chunk_var, width=8,
               bg=SURFACE, fg=TEXT, insertbackground=TEXT,
               buttonbackground=SURFACE, relief="flat",
               font=("Segoe UI", 10)).pack(side="left")
    tk.Label(chunk_row, text="  lower = more progress updates",
             bg=BG, fg=SUBTEXT, font=("Segoe UI", 8)).pack(side="left")

    # ── Save / Close ──────────────────────────────────────────────────────────
    ttk.Separator(root).pack(fill="x", padx=20, pady=12)

    save_lbl = tk.Label(root, text="", bg=BG, fg=GREEN, font=("Segoe UI", 8))
    save_lbl.pack()

    btn_row = tk.Frame(root, bg=BG)
    btn_row.pack(pady=4)

    def _save():
        cfg["source_lang"] = BY_NAME.get(src_var.get(), cfg["source_lang"])
        cfg["target_lang"] = BY_NAME.get(tgt_var.get(), cfg["target_lang"])
        cfg["chunk_size"]  = chunk_var.get()
        save_config(cfg)
        save_lbl.config(text="Settings saved.")
        root.after(2000, lambda: save_lbl.config(text=""))

    tk.Button(btn_row, text="Save Settings",
              bg=ACCENT, fg="#1e1e2e", font=("Segoe UI", 10, "bold"),
              relief="flat", padx=20, pady=6, cursor="hand2",
              command=_save).pack(side="left", padx=8)
    tk.Button(btn_row, text="Close",
              bg=SURFACE, fg=TEXT, font=("Segoe UI", 10),
              relief="flat", padx=20, pady=6, cursor="hand2",
              command=root.destroy).pack(side="left", padx=8)

    root.mainloop()


if __name__ == "__main__":
    main()
