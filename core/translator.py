"""TinyTranslate translation engine — Argos Translate (fully offline, no API key)."""
from typing import Callable, List, Optional, Tuple


def is_pack_installed(from_code: str, to_code: str) -> bool:
    """Return True if the language pack for this pair is already installed."""
    from argostranslate import translate as at
    installed = at.get_installed_languages()
    from_lang = next((l for l in installed if l.code == from_code), None)
    if not from_lang:
        return False
    return any(t.to_lang.code == to_code for t in from_lang.translations_from)


def translate(
    text: str,
    from_code: str,
    to_code: str,
    chunk_size: int = 1500,
    on_progress: Optional[Callable[[int, int], None]] = None,
) -> str:
    """Translate text offline. Calls on_progress(chunk_num, total) after each chunk."""
    from argostranslate import translate as at

    installed = at.get_installed_languages()
    from_lang = next((l for l in installed if l.code == from_code), None)
    to_lang   = next((l for l in installed if l.code == to_code),   None)

    if not from_lang:
        raise RuntimeError(
            f"Source language '{from_code}' is not installed.\n"
            "Open TinyTranslate Settings to install language packs."
        )
    if not to_lang:
        raise RuntimeError(
            f"Target language '{to_code}' is not installed.\n"
            "Open TinyTranslate Settings to install language packs."
        )

    engine = from_lang.get_translation(to_lang)
    if not engine:
        raise RuntimeError(
            f"No translation model found for {from_code} → {to_code}.\n"
            "Open TinyTranslate Settings and install the language pack."
        )

    chunks = _split_chunks(text, chunk_size)
    translated = []
    for i, chunk in enumerate(chunks):
        if on_progress:
            on_progress(i + 1, len(chunks))
        translated.append(engine.translate(chunk))
    return "\n\n".join(translated)


def _split_chunks(text: str, max_size: int) -> List[str]:
    """Split at paragraph boundaries, keeping chunks under max_size chars."""
    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for para in paragraphs:
        if current_len + len(para) > max_size and current:
            chunks.append("\n\n".join(current))
            current, current_len = [para], len(para)
        else:
            current.append(para)
            current_len += len(para) + 2

    if current:
        chunks.append("\n\n".join(current))

    return chunks or [text]


def list_installed_pairs() -> List[Tuple[str, str]]:
    """Return all installed (from_code, to_code) pairs."""
    from argostranslate import translate as at
    pairs = []
    for lang in at.get_installed_languages():
        for t in lang.translations_from:
            pairs.append((lang.code, t.to_lang.code))
    return sorted(pairs)


def install_language_pack(from_code: str, to_code: str):
    """Download and install an Argos language pack (requires internet, one-time)."""
    from argostranslate import package
    package.update_package_index()
    available = package.get_available_packages()
    pack = next(
        (p for p in available if p.from_code == from_code and p.to_code == to_code),
        None,
    )
    if not pack:
        raise RuntimeError(
            f"No package available for {from_code} → {to_code}.\n"
            "Check spelling or visit https://github.com/argosopentech/argos-translate "
            "for a list of supported pairs."
        )
    package.install_from_path(pack.download())
