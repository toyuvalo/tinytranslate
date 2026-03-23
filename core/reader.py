"""TinyTranslate file readers — supports .txt, .docx, .pdf"""
from pathlib import Path


def read_file(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".txt":
        return _read_txt(path)
    elif ext == ".docx":
        return _read_docx(path)
    elif ext == ".pdf":
        return _read_pdf(path)
    else:
        raise ValueError(f"Unsupported file type: {ext!r}. Supported: .txt .docx .pdf")


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _read_docx(path: str) -> str:
    from docx import Document
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        raise ValueError("No readable text found in this .docx file.")
    return "\n\n".join(paragraphs)


def _read_pdf(path: str) -> str:
    import pdfplumber
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t and t.strip():
                pages.append(t.strip())
    if not pages:
        raise ValueError(
            "Could not extract text from this PDF.\n"
            "It may be an image-only (scanned) document — OCR is not supported."
        )
    return "\n\n".join(pages)
