"""
TinyTranslate context menu registry manager.
Rebuilds the Explorer flyout from currently installed Argos packs.
Call register() after installing a new language pack.
"""
import os
import winreg
from pathlib import Path

_ROOT     = Path(__file__).parent.parent
_MENU     = "TinyTranslate"
_EXTS     = [".txt", ".docx", ".pdf"]
_PYTHONW  = str(_ROOT / ".venv" / "Scripts" / "pythonw.exe")
_MAIN     = str(_ROOT / "tinytranslate.py")
_SETTINGS = str(_ROOT / "settings.py")
_ICON     = str(_ROOT / "assets" / "icon.ico")


def _del_tree(hive, path):
    """Recursively delete all subkeys under path (no-op if missing)."""
    try:
        with winreg.OpenKey(hive, path) as k:
            while True:
                try:
                    sub = winreg.EnumKey(k, 0)
                    _del_tree(hive, f"{path}\\{sub}")
                    winreg.DeleteKey(k, sub)
                except OSError:
                    break
    except FileNotFoundError:
        pass


def _installed_targets(source_code: str) -> list:
    """Return [(code, name)] of installed target languages for source_code."""
    from core.translator import list_installed_pairs
    from config import LANGUAGES
    pairs = list_installed_pairs()
    return sorted(
        [(t, LANGUAGES.get(t, t.upper()))
         for s, t in pairs if s == source_code and t != source_code],
        key=lambda x: x[1],   # alphabetical by display name
    )


def register(source_code: str = "en") -> int:
    """
    Rebuild the HKCU context menu flyout from installed packs.
    Returns the number of languages added.
    """
    langs = _installed_targets(source_code)

    for ext in _EXTS:
        base  = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{_MENU}"
        shell = base + "\\shell"

        # Wipe old language subkeys so stale entries don't linger
        _del_tree(winreg.HKEY_CURRENT_USER, shell)

        # Top-level flyout entry
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, base) as k:
            winreg.SetValueEx(k, "MUIVerb",     0, winreg.REG_SZ, "Translate with TinyTranslate")
            winreg.SetValueEx(k, "SubCommands", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(k, "Icon",        0, winreg.REG_SZ, _ICON)

        # One item per installed language
        for code, name in langs:
            lkey = shell + f"\\lang_{code}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, lkey) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, name)
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, lkey + "\\command") as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ,
                    f'"{_PYTHONW}" "{_MAIN}" "%1" "{code}"')

        # "Add more languages..." always last
        mkey = shell + "\\zz_more"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, mkey) as k:
            winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "Add more languages...")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, mkey + "\\command") as k:
            winreg.SetValueEx(k, "", 0, winreg.REG_SZ,
                f'"{_PYTHONW}" "{_SETTINGS}"')

    return len(langs)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(_ROOT))
    from config import load_config
    src = load_config().get("source_lang", "en")
    n = register(src)
    print(f"[OK] Context menu updated — {n} language(s) registered.")
