"""Code Reviewer Agent — CLI entry point."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.table import Table
from rich.theme import Theme

from code_analyzer import (
    CodeAnalyzerError,
    EmptyFileError,
    InvalidPathError,
    ReviewContext,
    UnsupportedFileTypeError,
    build_review_context,
    read_folder,
    read_pasted_code,
    read_single_file,
)
from groq_client import GroqClient, GroqClientError, GroqConfigurationError

load_dotenv()

THEME = Theme(
    {
        "info": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "bold red",
        "title": "bold magenta",
        "critical": "bold red",
        "high": "red",
        "medium": "yellow",
        "low": "dim",
    }
)
console = Console(theme=THEME, force_terminal=True)

SECTION_ORDER = [
    "File Information",
    "Quality Scores",
    "Issues Found",
    "Improvement Suggestions",
    "Final Summary",
]

SEVERITY_COLORS = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review source code and provide professional feedback.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File or folder path to review (omit to paste code interactively)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        help="Groq model to use for review",
    )
    return parser.parse_args()


def prompt_for_code() -> str:
    console.print(
        "[info]Paste your source code below. Press Enter twice when finished.[/info]"
    )

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines)


def split_review_sections(review: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(review))
    if not matches:
        return [("Review", review.strip())]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(review)
        body = review[start:end].strip()
        sections.append((title, body))
    return sections


def parse_scores(body: str) -> list[tuple[str, int]]:
    scores: list[tuple[str, int]] = []
    for line in body.splitlines():
        match = re.search(r"([A-Za-z][\w\s]*?)\s*:?\s*(\d{1,3})\s*/\s*100", line)
        if match:
            name = match.group(1).strip()
            value = min(100, max(0, int(match.group(2))))
            scores.append((name, value))
    return scores


def score_bar(value: int, width: int = 20) -> str:
    filled = int(value / 100 * width)
    return "#" * filled + "-" * (width - filled)


def display_header(context: ReviewContext) -> None:
    target_label = "Folder" if context.is_folder else "File"
    console.print()
    console.print(
        Panel.fit(
            f"[title]Code Reviewer[/title]\n"
            f"[info]{target_label}:[/info] [bold]{context.target}[/bold]\n"
            f"[info]Files:[/info] {len(context.files)}  "
            f"[info]Lines:[/info] {context.total_lines}  "
            f"[info]Language:[/info] {context.primary_language}",
            border_style="magenta",
        )
    )
    console.print()


def display_file_table(context: ReviewContext) -> None:
    table = Table(title="Files Reviewed", show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Language")
    table.add_column("Lines", justify="right")
    for source in context.files:
        table.add_row(source.path, source.language, str(source.lines_of_code))
    console.print(table)
    console.print()


def display_scores_table(body: str) -> None:
    scores = parse_scores(body)
    if not scores:
        console.print(Markdown(body))
        console.print()
        return

    table = Table(title="Quality Scores", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Bar")
    for name, value in scores:
        color = "green" if value >= 80 else "yellow" if value >= 60 else "red"
        table.add_row(name, f"[{color}]{value}/100[/{color}]", score_bar(value))
    console.print(table)
    console.print()


def extract_issues(body: str) -> list[dict[str, str]]:
    if "no significant issues" in body.lower():
        return []

    pattern = re.compile(
        r"(?:-\s*)?(?:\*\*Severity\*\*|Severity):\s*(critical|high|medium|low)\s*"
        r"(?:-\s*)?(?:\*\*Description\*\*|Description):\s*(.*?)"
        r"(?:-\s*)?(?:\*\*Location\*\*|Location):\s*(.*?)"
        r"(?:-\s*)?(?:\*\*Recommendation\*\*|Recommendation):\s*(.*?)"
        r"(?=(?:-\s*)?(?:\*\*Severity\*\*|Severity):|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    issues: list[dict[str, str]] = []
    for match in pattern.finditer(body):
        issues.append(
            {
                "severity": match.group(1).lower(),
                "description": " ".join(match.group(2).split()),
                "location": " ".join(match.group(3).split()),
                "recommendation": " ".join(match.group(4).split()),
            }
        )
    return issues


def display_issues(body: str) -> None:
    issues = extract_issues(body)
    if not issues and "no significant issues" in body.lower():
        console.print(Panel(Markdown(body), border_style="green", title="Issues Found"))
        console.print()
        return

    if not issues:
        console.print(Markdown(body))
        console.print()
        return

    table = Table(title="Issues Found", show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Severity", width=10)
    table.add_column("Description", ratio=2)
    table.add_column("Location", ratio=1)
    table.add_column("Recommendation", ratio=2)

    for issue in issues:
        severity = issue["severity"]
        color = SEVERITY_COLORS.get(severity, "info")
        table.add_row(
            f"[{color}]{severity.upper()}[/{color}]",
            issue["description"],
            issue["location"],
            issue["recommendation"],
        )

    console.print(table)
    console.print()


def display_section(title: str, body: str, context: ReviewContext | None = None) -> None:
    console.print(Rule(f"[title]{title}[/title]", style="magenta"))

    if title == "File Information" and context:
        display_file_table(context)
        if body.strip():
            console.print(Markdown(body))
            console.print()
    elif title == "Quality Scores":
        display_scores_table(body)
    elif title == "Issues Found":
        display_issues(body)
    else:
        console.print(Markdown(body))
        console.print()


def display_sections(sections: list[tuple[str, str]], context: ReviewContext) -> None:
    section_map = dict(sections)
    ordered_titles = [title for title in SECTION_ORDER if title in section_map]
    remaining = [title for title, _ in sections if title not in ordered_titles]

    for title in ordered_titles + remaining:
        display_section(title, section_map[title], context if title == "File Information" else None)


def load_context(path: str | None) -> ReviewContext:
    if not path:
        code = prompt_for_code()
        return read_pasted_code(code)

    resolved = Path(path)
    if resolved.is_file():
        return read_single_file(resolved)
    if resolved.is_dir():
        return read_folder(resolved)
    raise InvalidPathError(f"Path not found: {path}")


def run(path: str | None, model: str) -> int:
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Reading source code...", total=None)
            context = load_context(path)

        display_header(context)
        code_context = build_review_context(context)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Generating code review with Groq...", total=None)
            groq = GroqClient(model=model)
            review = groq.review_code(code_context)

        sections = split_review_sections(review)
        display_sections(sections, context)

        console.print(
            Panel(
                "[success]Review complete.[/success] See the sections above for scores, issues, and recommendations.",
                border_style="green",
            )
        )
        return 0

    except InvalidPathError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except EmptyFileError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except UnsupportedFileTypeError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqConfigurationError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except CodeAnalyzerError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqClientError as exc:
        console.print(f"[error]Groq error:[/error] {exc}")
        return 1
    except KeyboardInterrupt:
        console.print("\n[warning]Review cancelled.[/warning]")
        return 130


def main() -> None:
    args = parse_args()
    sys.exit(run(args.path, args.model))


if __name__ == "__main__":
    main()
