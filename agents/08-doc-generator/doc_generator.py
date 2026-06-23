"""Project description reader and documentation orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from groq_client import GroqClient

OUTPUT_FILENAME = "README_generated.md"


class DocGeneratorError(Exception):
    """Base error for documentation generator operations."""


class EmptyInputError(DocGeneratorError):
    """Raised when project description input is empty."""


class InvalidPathError(DocGeneratorError):
    """Raised when a file path is invalid."""


@dataclass
class ProjectInput:
    description: str
    source: str


def read_description_from_file(path: Path) -> ProjectInput:
    if not path.exists():
        raise InvalidPathError(f"File not found: {path}")
    if not path.is_file():
        raise InvalidPathError(f"Not a file: {path}")

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise EmptyInputError(f"File is empty: {path}")

    return ProjectInput(description=content, source=str(path))


def read_description_from_text(text: str, source: str = "command line") -> ProjectInput:
    content = text.strip()
    if not content:
        raise EmptyInputError("Project description cannot be empty.")
    return ProjectInput(description=content, source=source)


def build_user_message(project: ProjectInput) -> str:
    return (
        "Generate complete technical documentation for the following project description.\n\n"
        f"---\n{project.description}\n---"
    )


def save_documentation(content: str, output_dir: Path | None = None) -> Path:
    directory = output_dir or Path.cwd()
    output_path = directory / OUTPUT_FILENAME
    output_path.write_text(content.strip() + "\n", encoding="utf-8")
    return output_path


def generate_documentation(
    project: ProjectInput,
    groq: GroqClient,
    output_dir: Path | None = None,
) -> tuple[str, Path]:
    """Generate documentation via Groq and save to README_generated.md."""
    user_message = build_user_message(project)
    documentation = groq.generate_documentation(user_message)
    output_path = save_documentation(documentation, output_dir)
    return documentation, output_path
