"""Source code reader and context builder for code review."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

SUPPORTED_EXTENSIONS: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".sql": "SQL",
    ".sh": "Shell",
    ".bash": "Shell",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".md": "Markdown",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "htmlcov",
    ".tox",
    "eggs",
    ".eggs",
}

MAX_FOLDER_FILES = 25
MAX_FILE_CHARS = 12000
MAX_TOTAL_CHARS = 80000


class CodeAnalyzerError(Exception):
    """Base error for code analyzer operations."""


class InvalidPathError(CodeAnalyzerError):
    """Raised when a file or folder path is invalid."""


class EmptyFileError(CodeAnalyzerError):
    """Raised when a file has no content."""


class UnsupportedFileTypeError(CodeAnalyzerError):
    """Raised when a file type is not supported for review."""


@dataclass
class SourceFile:
    path: str
    language: str
    content: str
    lines_of_code: int


@dataclass
class ReviewContext:
    target: str
    files: list[SourceFile] = field(default_factory=list)
    is_folder: bool = False

    @property
    def total_lines(self) -> int:
        return sum(f.lines_of_code for f in self.files)

    @property
    def primary_language(self) -> str:
        if not self.files:
            return "Unknown"
        counts: dict[str, int] = {}
        for f in self.files:
            counts[f.language] = counts.get(f.language, 0) + f.lines_of_code
        return max(counts, key=counts.get)


def detect_language(path: Path) -> str:
    return SUPPORTED_EXTENSIONS.get(path.suffix.lower(), "Unknown")


def count_lines(content: str) -> int:
    return len(content.splitlines())


def read_source_file(path: Path, base_dir: Path | None = None) -> SourceFile:
    if not path.exists():
        raise InvalidPathError(f"File not found: {path}")
    if not path.is_file():
        raise InvalidPathError(f"Not a file: {path}")

    language = detect_language(path)
    if language == "Unknown":
        raise UnsupportedFileTypeError(
            f"Unsupported file type '{path.suffix}'. "
            f"Supported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    content = path.read_text(encoding="utf-8", errors="replace")
    if not content.strip():
        raise EmptyFileError(f"File is empty: {path}")

    if len(content) > MAX_FILE_CHARS:
        content = content[:MAX_FILE_CHARS] + "\n... [truncated]"

    display_path = str(path.relative_to(base_dir)) if base_dir else str(path)
    return SourceFile(
        path=display_path,
        language=language,
        content=content,
        lines_of_code=count_lines(content),
    )


def collect_folder_files(folder: Path) -> list[Path]:
    collected: list[Path] = []
    for item in sorted(folder.rglob("*")):
        if not item.is_file():
            continue
        if any(part in SKIP_DIRS for part in item.parts):
            continue
        if item.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        collected.append(item)
        if len(collected) >= MAX_FOLDER_FILES:
            break
    return collected


def read_folder(folder_path: Path) -> ReviewContext:
    folder = folder_path.resolve()
    if not folder.exists():
        raise InvalidPathError(f"Folder not found: {folder_path}")
    if not folder.is_dir():
        raise InvalidPathError(f"Not a folder: {folder_path}")

    paths = collect_folder_files(folder)
    if not paths:
        raise InvalidPathError(
            f"No supported source files found in '{folder_path}'. "
            "Try a folder containing .py, .js, .ts, or other supported files."
        )

    files: list[SourceFile] = []
    total_chars = 0
    for path in paths:
        try:
            source = read_source_file(path, base_dir=folder)
        except EmptyFileError:
            continue
        if total_chars + len(source.content) > MAX_TOTAL_CHARS:
            break
        files.append(source)
        total_chars += len(source.content)

    if not files:
        raise EmptyFileError(f"All source files in '{folder_path}' are empty.")

    return ReviewContext(target=str(folder_path), files=files, is_folder=True)


def read_single_file(file_path: Path) -> ReviewContext:
    resolved = file_path.resolve()
    source = read_source_file(resolved)
    source.path = file_path.name
    return ReviewContext(target=file_path.name, files=[source], is_folder=False)


def read_pasted_code(code: str, filename: str = "pasted_code.py") -> ReviewContext:
    if not code.strip():
        raise EmptyFileError("No code provided.")

    path = Path(filename)
    language = detect_language(path)
    if language == "Unknown":
        language = "Unknown"

    if len(code) > MAX_FILE_CHARS:
        code = code[:MAX_FILE_CHARS] + "\n... [truncated]"

    source = SourceFile(
        path=filename,
        language=language,
        content=code,
        lines_of_code=count_lines(code),
    )
    return ReviewContext(target=filename, files=[source], is_folder=False)


def build_review_context(context: ReviewContext) -> str:
    """Format source files into a prompt for the LLM."""
    lines: list[str] = []
    if context.is_folder:
        lines.append(f"Review target: folder '{context.target}'")
        lines.append(f"Files included: {len(context.files)} (max {MAX_FOLDER_FILES})")
    else:
        lines.append(f"Review target: file '{context.target}'")

    lines.append(f"Primary language: {context.primary_language}")
    lines.append(f"Total lines of code: {context.total_lines}")
    lines.append("")

    for source in context.files:
        lines.append(f"--- FILE: {source.path} ({source.language}, {source.lines_of_code} lines) ---")
        lines.append(source.content)
        lines.append("")

    return "\n".join(lines)
