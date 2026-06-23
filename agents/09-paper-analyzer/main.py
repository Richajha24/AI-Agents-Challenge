"""Research Paper Analyzer Agent — CLI entry point."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.theme import Theme

from groq_client import GroqClient, GroqClientError, GroqConfigurationError
from paper_parser import (
    EmptyInputError,
    InvalidPathError,
    PaperParserError,
    PdfParseError,
    UnsupportedFileTypeError,
    build_paper_context,
    read_paper_from_file,
)

load_dotenv()


def configure_stdio() -> None:
    """Use UTF-8 on Windows so Rich can render markdown correctly."""
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

OUTPUT_FILENAME = "paper_analysis_report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a research paper (PDF, .txt, or .md) and generate a structured report."
    )
    parser.add_argument(
        "-p",
        "--paper",
        dest="paper_path",
        help="Path to a research paper file (PDF, .txt, or .md)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where paper_analysis_report.md will be saved (default: current directory)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        help="Groq model to use for analysis",
    )
    return parser.parse_args()


def prompt_for_paper_path() -> str:
    console.print("[info]Enter the path to the research paper (PDF, .txt, or .md).[/info]")
    return console.input("[bold]Paper path:[/bold] ").strip()


def split_sections(report: str) -> list[tuple[str, str]]:
    # Split by top-level headings starting with '# '
    lines = report.splitlines()
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_body: list[str] = []

    for line in lines:
        if line.startswith("# ") and not line.startswith("## ") and not line.startswith("### "):
            if current_title is not None:
                sections.append((current_title, "\n".join(current_body).strip()))
            current_title = line[2:].strip()
            current_body = []
        else:
            current_body.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_body).strip()))

    if not sections:
        return [("Report", report.strip())]
    return sections


def display_report(report: str) -> None:
    sections = split_sections(report)
    for title, body in sections:
        console.print(Rule(f"[title]{title}[/title]", style="magenta"))
        if body:
            console.print(Markdown(body))
        console.print()


def save_report(report: str, output_dir: Path) -> Path:
    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(report.strip() + "\n", encoding="utf-8")
    return output_path


def run(paper_path: str | None, output_dir: str, model: str) -> int:
    try:
        resolved_paper = paper_path or prompt_for_paper_path()
        if not resolved_paper:
            raise InvalidPathError("No paper path provided.")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Reading paper...", total=None)
            paper = read_paper_from_file(Path(resolved_paper))

        console.print()
        console.print(
            Panel.fit(
                f"[title]Research Paper Analyzer[/title]\n"
                f"[info]Paper:[/info] [bold]{paper.source}[/bold] ([info]{paper.file_type}[/info])",
                border_style="magenta",
            )
        )
        console.print()

        context = build_paper_context(paper)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Analyzing paper with Groq...", total=None)
            groq = GroqClient(model=model)
            report = groq.analyze_paper(context)

        display_report(report)

        output_path = save_report(report, Path(output_dir))
        console.print(
            Panel(
                f"[success]Report saved to[/success] [bold]{output_path.resolve()}[/bold]",
                border_style="green",
            )
        )
        return 0

    except InvalidPathError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except UnsupportedFileTypeError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except PdfParseError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except EmptyInputError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqConfigurationError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqClientError as exc:
        console.print(f"[error]Groq error:[/error] {exc}")
        return 1
    except PaperParserError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except KeyboardInterrupt:
        console.print("\n[warning]Analysis cancelled.[/warning]")
        return 130


def main() -> None:
    args = parse_args()
    sys.exit(run(args.paper_path, args.output_dir, args.model))


if __name__ == "__main__":
    main()

