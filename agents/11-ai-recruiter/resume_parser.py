"""Resume and job description reader for hiring analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

SUPPORTED_RESUME_EXTENSIONS = {".pdf", ".txt", ".md"}
SUPPORTED_JOB_EXTENSIONS = {".txt", ".md"}


class ResumeParserError(Exception):
    """Base error for resume parser operations."""


class InvalidPathError(ResumeParserError):
    """Raised when a file path is invalid."""


class EmptyInputError(ResumeParserError):
    """Raised when input content is empty."""


class UnsupportedFileTypeError(ResumeParserError):
    """Raised when a file type is not supported."""


class PdfParseError(ResumeParserError):
    """Raised when a PDF cannot be parsed."""


@dataclass
class ResumeInput:
    content: str
    source: str
    file_type: str


@dataclass
class JobDescriptionInput:
    content: str
    source: str


@dataclass
class EvaluationInput:
    resume: ResumeInput
    job_description: JobDescriptionInput


def _read_text_file(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidPathError(
            f"Could not read text file (unsupported encoding): {path}"
        ) from exc
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
            f"No extractable text found in PDF: {path}. "
            "The file may be image-only or scanned."
        )
    return content


def read_resume_from_file(path: Path) -> ResumeInput:
    if not path.exists():
        raise InvalidPathError(f"Resume file not found: {path}")
    if not path.is_file():
        raise InvalidPathError(f"Not a file: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_RESUME_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported resume format '{suffix}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_RESUME_EXTENSIONS))}"
        )

    if suffix == ".pdf":
        content = _read_pdf_file(path)
        file_type = "PDF"
    else:
        content = _read_text_file(path)
        if not content:
            raise EmptyInputError(f"Resume file is empty: {path}")
        file_type = suffix.lstrip(".").upper()

    return ResumeInput(content=content, source=str(path), file_type=file_type)


def read_job_from_file(path: Path) -> JobDescriptionInput:
    if not path.exists():
        raise InvalidPathError(f"Job description file not found: {path}")
    if not path.is_file():
        raise InvalidPathError(f"Not a file: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_JOB_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported job description format '{suffix}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_JOB_EXTENSIONS))}"
        )

    content = _read_text_file(path)
    if not content:
        raise EmptyInputError(f"Job description file is empty: {path}")

    return JobDescriptionInput(content=content, source=str(path))


def read_job_from_text(text: str, source: str = "command line") -> JobDescriptionInput:
    content = text.strip()
    if not content:
        raise EmptyInputError("Job description cannot be empty.")
    return JobDescriptionInput(content=content, source=source)


def build_evaluation_context(evaluation: EvaluationInput) -> str:
    return (
        "Analyze the following candidate resume against the job description "
        "and produce a complete hiring evaluation.\n\n"
        f"--- RESUME ({evaluation.resume.source}, {evaluation.resume.file_type}) ---\n"
        f"{evaluation.resume.content}\n"
        f"--- END RESUME ---\n\n"
        f"--- JOB DESCRIPTION ({evaluation.job_description.source}) ---\n"
        f"{evaluation.job_description.content}\n"
        f"--- END JOB DESCRIPTION ---"
    )
