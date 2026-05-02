"""
TinyTranslate config loader/saver.
config.json lives next to this file and is gitignored — never committed.
"""
import json
import os

VERSION = "1.0.2"

# Single source of truth for language names — used by settings.py and core/registry.py
LANGUAGES = {
    "af": "Afrikaans",   "ar": "Arabic",       "az": "Azerbaijani",
    "be": "Belarusian",  "bg": "Bulgarian",     "ca": "Catalan",
    "cs": "Czech",       "cy": "Welsh",         "da": "Danish",
    "de": "German",      "el": "Greek",         "en": "English",
    "eo": "Esperanto",   "es": "Spanish",       "et": "Estonian",
    "eu": "Basque",      "fa": "Persian",       "fi": "Finnish",
    "fr": "French",      "ga": "Irish",         "gl": "Galician",
    "gu": "Gujarati",    "he": "Hebrew",        "hi": "Hindi",
    "hr": "Croatian",    "hu": "Hungarian",     "hy": "Armenian",
    "id": "Indonesian",  "is": "Icelandic",     "it": "Italian",
    "ja": "Japanese",    "ka": "Georgian",      "ko": "Korean",
    "lt": "Lithuanian",  "lv": "Latvian",       "mk": "Macedonian",
    "ms": "Malay",       "mt": "Maltese",       "nb": "Norwegian",
    "nl": "Dutch",       "pl": "Polish",        "pt": "Portuguese",
    "ro": "Romanian",    "ru": "Russian",       "sk": "Slovak",
    "sl": "Slovenian",   "sq": "Albanian",      "sr": "Serbian",
    "sv": "Swedish",     "th": "Thai",          "tl": "Filipino",
    "tr": "Turkish",     "uk": "Ukrainian",     "ur": "Urdu",
    "vi": "Vietnamese",  "zh": "Chinese",
}

_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_DIR, "config.json")

DEFAULTS = {
    "source_lang": "en",
    "target_lang": "fr",
    "chunk_size": 1500,
}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        cfg = DEFAULTS.copy()
        save_config(cfg)
        return cfg
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    for k, v in DEFAULTS.items():
        if k not in cfg:
            cfg[k] = v
    return cfg


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
