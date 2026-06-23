"""Feedback input parsing and context building."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class FeedbackParserError(Exception):
    """Base error for feedback parser operations."""


class InvalidPathError(FeedbackParserError):
    """Raised when a file path is invalid."""


class EmptyInputError(FeedbackParserError):
    """Raised when input content is empty."""


class MalformedFeedbackError(FeedbackParserError):
    """Raised when feedback input formatting is unusable."""


@dataclass
class FeedbackInput:
    content: str
    source: str
    mode: str  # "file" or "interactive"


SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md", ".csv"}


def read_feedback_from_file(path: Path) -> FeedbackInput:
    if not path.exists():
        raise InvalidPathError(f"Feedback file not found: {path}")
    if not path.is_file():
        raise InvalidPathError(f"Not a file: {path}")

    suffix = path.suffix.lower()
    if suffix and suffix not in SUPPORTED_TEXT_EXTENSIONS:
        # keep simple: README mentions .txt; allow .md for robustness
        raise InvalidPathError(
            f"Unsupported feedback file format '{suffix}'. Supported formats: {', '.join(sorted(SUPPORTED_TEXT_EXTENSIONS))}"
        )

    try:
        content = path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError as exc:
        raise InvalidPathError(f"Could not read feedback file (unsupported encoding): {path}") from exc

    if not content:
        raise EmptyInputError(f"Feedback file is empty: {path}")

    return FeedbackInput(content=content, source=str(path), mode="file")


def normalize_feedback_entries(raw: str) -> list[str]:
    """Split raw text into feedback entries.

    Accepts either:
    - newline-separated paragraphs
    - one feedback per line (best-effort)
    - comma-separated items

    Returns a non-empty list.
    """
    text = raw.strip()
    if not text:
        raise EmptyInputError("No feedback provided.")

    # Try splitting by blank lines first.
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    if len(blocks) >= 2:
        return blocks

    # Fallback: split by single newlines; keep small lines as potential entries.
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) >= 2:
        return lines

    # Fallback: comma-separated
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(parts) >= 2:
        return parts

    # Single entry
    return [text]


def build_feedback_context(feedback: FeedbackInput) -> str:
    entries = normalize_feedback_entries(feedback.content)

    # Basic sanity: avoid sending absurdly long prompts.
    # We keep it lightweight; LLM will truncate if needed.
    formatted_entries = []
    for i, entry in enumerate(entries, start=1):
        formatted_entries.append(f"[FEEDBACK {i}]\n{entry}")

    return (
        "Analyze the following feedback entries and produce the report in markdown.\n\n"
        f"--- SOURCE ({feedback.source}) / MODE ({feedback.mode}) ---\n"
        + "\n\n".join(formatted_entries)
        + "\n--- END FEEDBACK ---"
    )

