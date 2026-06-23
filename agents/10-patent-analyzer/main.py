"""Patent Analyzer Agent — CLI entry point."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.theme import Theme
from rich.markdown import Markdown

from groq_client import GroqClient, GroqClientError, GroqConfigurationError
from patent_parser import (
    EmptyInputError,
    InvalidPathError,
    PdfParseError,
    PatentParserError,
    UnsupportedFileTypeError,
    PatentInput,
    read_patent_from_file,
)

load_dotenv()


def configure_stdio() -> None:
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
        description="Analyze a patent PDF or patent text and generate structured technical/business insights.",
    )
    parser.add_argument(
        "-p",
        "--patent",
        dest="patent_path",
        help="Path to patent file (PDF, .txt, or .md)",
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


def display_header(patent: PatentInput) -> None:
    console.print()
    console.print(
        Panel.fit(
            f"[title]Patent Analyzer[/title]\n"
            f"[info]Patent:[/info] [bold]{patent.source}[/bold] "
            f"([info]{patent.file_type}[/info])",
            border_style="magenta",
        )
    )
    console.print()


def save_report(report: str, output_dir: Path) -> Path:
    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(report.strip() + "\n", encoding="utf-8")
    return output_path


def run(patent_path: str | None, output_dir: str, model: str) -> int:
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Reading patent...", total=None)
            patent = read_patent_from_file(Path(patent_path) if patent_path else Path(""))

        display_header(patent)

        context = (
            "Analyze the following patent document and produce the required structured output.\n\n"
            f"--- PATENT ({patent.source}, {patent.file_type}) ---\n"
            f"{patent.content}\n"
            "--- END PATENT ---"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Generating patent analysis with Groq...", total=None)
            groq = GroqClient(model=model)
            report = groq.analyze_patent(context)

        # Required markdown headings are produced by the system prompt.
        console.print(Rule("Analysis", style="magenta"))
        console.print(Markdown(report))

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
    except EmptyInputError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except UnsupportedFileTypeError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except PdfParseError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqConfigurationError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqClientError as exc:
        console.print(f"[error]Groq error:[/error] {exc}")
        return 1
    except PatentParserError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except KeyboardInterrupt:
        console.print("\n[warning]Analysis cancelled.[/warning]")
        return 130


def main() -> None:
    args = parse_args()
    if not args.patent_path:
        console.print("[error]Please provide --patent / -p with a PDF or text patent file.[/error]")
        sys.exit(2)
    sys.exit(run(args.patent_path, args.output_dir, args.model))


if __name__ == "__main__":
    main()

