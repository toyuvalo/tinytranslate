"""TinyTranslate GUI helpers — Catppuccin Mocha theme."""
import tkinter as tk
from tkinter import messagebox

BG      = "#1e1e2e"
SURFACE = "#313244"
ACCENT  = "#89b4fa"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
GOLD    = "#f9e2af"


class ProgressWindow:
    """Small loading window shown during translation."""

    def __init__(self, filename: str):
        self.root = tk.Tk()
        self.root.title("TinyTranslate")
        self.root.geometry("380x100")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)
        self.root.eval("tk::PlaceWindow . center")

        tk.Label(
            self.root, text="TinyTranslate",
            bg=BG, fg=ACCENT, font=("Segoe UI", 12, "bold"),
        ).pack(pady=(16, 3))

        self._status = tk.StringVar(value=f"Reading {filename}...")
        tk.Label(
            self.root, textvariable=self._status,
            bg=BG, fg=SUBTEXT, font=("Segoe UI", 9),
        ).pack()

        self.root.update()

    def update(self, message: str):
        self._status.set(message)
        self.root.update()

    def close(self):
        try:
            self.root.destroy()
        except Exception:
            pass


def alert(level: str, title: str, msg: str):
    """Show a modal message box (topmost)."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    if level == "error":
        messagebox.showerror(title, msg, parent=root)
    elif level == "warning":
        messagebox.showwarning(title, msg, parent=root)
    else:
        messagebox.showinfo(title, msg, parent=root)
    root.destroy()
