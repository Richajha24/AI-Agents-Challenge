"""Patent input parsing (PDF and text)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

SUPPORTED_PATENT_EXTENSIONS = {".pdf", ".txt", ".md"}


class PatentParserError(Exception):
    """Base error for patent parser operations."""


class InvalidPathError(PatentParserError):
    """Raised when a file path is invalid."""


class EmptyInputError(PatentParserError):
    """Raised when extracted input content is empty."""


class UnsupportedFileTypeError(PatentParserError):
    """Raised when a file type is not supported."""


class PdfParseError(PatentParserError):
    """Raised when a PDF cannot be parsed."""


@dataclass
class PatentInput:
    content: str
    source: str
    file_type: str


def _read_text_file(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidPathError(f"Could not read text file (unsupported encoding): {path}") from exc
    return content.strip()


def _read_pdf_file(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
    except PdfReadError as exc:
        raise PdfParseError(f"Invalid or corrupted PDF: {path}") from exc
    except OSError as exc:
        raise InvalidPathError(f"Could not read PDF file: {path}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise PdfParseError(f"PDF is encrypted and cannot be read: {path}") from exc

    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())

    content = "\n\n".join(pages).strip()
    if not content:
        raise EmptyInputError(
            f"No extractable text found in PDF: {path}. The file may be image-only or scanned."
        )
    return content


def read_patent_from_file(path: Path) -> PatentInput:
    if not path.exists():
        raise InvalidPathError(f"Patent file not found: {path}")
    if not path.is_file():
        raise InvalidPathError(f"Not a file: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_PATENT_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported patent format '{suffix}'. Supported formats: {', '.join(sorted(SUPPORTED_PATENT_EXTENSIONS))}"
        )

    if suffix == ".pdf":
        content = _read_pdf_file(path)
        file_type = "PDF"
    else:
        content = _read_text_file(path)
        if not content:
            raise EmptyInputError(f"Patent file is empty: {path}")
        file_type = suffix.lstrip(".").upper()

    return PatentInput(content=content, source=str(path), file_type=file_type)

