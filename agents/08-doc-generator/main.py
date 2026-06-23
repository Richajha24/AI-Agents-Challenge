"""Documentation Generator Agent — CLI entry point."""

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
from rich.theme import Theme

from doc_generator import (
    DocGeneratorError,
    EmptyInputError,
    InvalidPathError,
    ProjectInput,
    generate_documentation,
    read_description_from_file,
    read_description_from_text,
)
from groq_client import GroqClient, GroqClientError, GroqConfigurationError

load_dotenv()


def configure_stdio() -> None:
    """Use UTF-8 on Windows so Rich can render markdown tree characters."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


configure_stdio()

THEME = Theme(
    {
        "info": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "bold red",
        "title": "bold magenta",
    }
)
console = Console(theme=THEME, force_terminal=True)

SECTION_ORDER = [
    "Project Overview",
    "Features",
    "Installation Guide",
    "Usage Guide",
    "Folder Structure Explanation",
    "Architecture Overview",
    "API Documentation",
    "Future Improvements",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate professional technical documentation from a project description.",
    )
    parser.add_argument(
        "description",
        nargs="?",
        help="Project description text (omit to read from file or interactive input)",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="file_path",
        help="Path to a text file containing the project description",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where README_generated.md will be saved (default: current directory)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        help="Groq model to use for documentation generation",
    )
    return parser.parse_args()


def prompt_for_description() -> str:
    console.print(
        "[info]Enter your project description below. "
        "Press Enter twice when finished.[/info]"
    )
    lines: list[str] = []
    blank_count = 0
    while True:
        try:
            line = console.input("")
        except EOFError:
            break
        if line == "":
            blank_count += 1
            if blank_count >= 2 and lines:
                break
            if not lines:
                continue
            lines.append("")
        else:
            blank_count = 0
            lines.append(line)
    return "\n".join(lines).strip()


def load_project_input(description: str | None, file_path: str | None) -> ProjectInput:
    if file_path:
        return read_description_from_file(Path(file_path))
    if description:
        return read_description_from_text(description, source="command line argument")
    text = prompt_for_description()
    return read_description_from_text(text, source="interactive input")


def split_documentation_sections(documentation: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(documentation))
    if not matches:
        return [("Documentation", documentation.strip())]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(documentation)
        body = documentation[start:end].strip()
        sections.append((title, body))
    return sections


def display_header(project: ProjectInput) -> None:
    preview = project.description.replace("\n", " ")
    if len(preview) > 120:
        preview = preview[:117] + "..."
    console.print()
    console.print(
        Panel.fit(
            f"[title]Documentation Generator[/title]\n"
            f"[info]Source:[/info] [bold]{project.source}[/bold]\n"
            f"[info]Description:[/info] {preview}",
            border_style="magenta",
        )
    )
    console.print()


def display_sections(sections: list[tuple[str, str]]) -> None:
    section_map = dict(sections)
    ordered_titles = [title for title in SECTION_ORDER if title in section_map]
    remaining = [title for title, _ in sections if title not in ordered_titles]

    for title in ordered_titles + remaining:
        body = section_map[title]
        console.print(Rule(f"[title]{title}[/title]", style="magenta"))
        console.print(Markdown(body))
        console.print()


def run(
    description: str | None,
    file_path: str | None,
    output_dir: str,
    model: str,
) -> int:
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Reading project description...", total=None)
            project = load_project_input(description, file_path)

        display_header(project)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Generating documentation with Groq...", total=None)
            groq = GroqClient(model=model)
            documentation, output_path = generate_documentation(
                project, groq, Path(output_dir)
            )

        sections = split_documentation_sections(documentation)
        display_sections(sections)

        console.print(
            Panel(
                f"[success]Documentation saved to[/success] [bold]{output_path.resolve()}[/bold]",
                border_style="green",
            )
        )
        return 0

    except InvalidPathError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except EmptyInputError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqConfigurationError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except DocGeneratorError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqClientError as exc:
        console.print(f"[error]Groq error:[/error] {exc}")
        return 1
    except KeyboardInterrupt:
        console.print("\n[warning]Documentation generation cancelled.[/warning]")
        return 130


def main() -> None:
    args = parse_args()
    sys.exit(run(args.description, args.file_path, args.output_dir, args.model))


if __name__ == "__main__":
    main()
