"""Agent 12 — Feedback Analyzer (CLI)."""

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

from feedback_parser import (
    EmptyInputError,
    FeedbackParserError,
    InvalidPathError,
    build_feedback_context,
    read_feedback_from_file,
)
from groq_client import GroqClient, GroqClientError, GroqConfigurationError

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

OUTPUT_FILENAME = "feedback_analysis_report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze feedback and generate actionable insights (Rich + Groq).")
    parser.add_argument(
        "-f",
        "--feedback-file",
        dest="feedback_file",
        help="Path to a feedback text file (one or many entries)",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive mode (paste feedback, end with an empty line)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where feedback_analysis_report.md will be saved (default: current directory)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME") or os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile",
        help="Groq model to use for analysis",
    )
    return parser.parse_args()


def prompt_for_feedback_text() -> str:
    console.print("[info]Paste feedback below. Submit an empty line to finish.[/info]")
    lines: list[str] = []
    while True:
        line = console.input()
        if not line.strip():
            break
        lines.append(line)
    raw = "\n".join(lines).strip()
    return raw


def render_markdown_report(report_md: str) -> None:
    # The LLM output already includes markdown headings; render as panels/sections.
    # Keep it simple and robust: render full markdown + a title.
    console.print(
        Panel.fit(
            "[title]Feedback Analyzer[/title]\n"
            "[info]Generating insights from feedback[/info]",
            border_style="magenta",
        )
    )

    console.print()
    console.print(Rule("[title]Analysis Report[/title]", style="magenta"))
    console.print(Markdown(report_md))


def save_report(report_md: str, output_dir: Path) -> Path:
    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(report_md.strip() + "\n", encoding="utf-8")
    return output_path


def run(feedback_file: str | None, interactive: bool, output_dir: str, model: str) -> int:
    try:
        if not feedback_file and not interactive:
            # Default to interactive mode if nothing provided.
            interactive = True

        if feedback_file:
            resolved = Path(feedback_file)
        else:
            resolved = None

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Reading feedback...", total=None)
            if resolved is not None:
                feedback_input = read_feedback_from_file(resolved)
            else:
                from feedback_parser import FeedbackInput

                raw = prompt_for_feedback_text()
                feedback_input = FeedbackInput(content=raw, source="interactive", mode="interactive")
                if not feedback_input.content.strip():
                    raise EmptyInputError("No feedback entered.")

        context = build_feedback_context(feedback_input)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Analyzing feedback with Groq...", total=None)
            groq = GroqClient(model=model)
            report_md = groq.analyze_feedback(context)

        render_markdown_report(report_md)

        output_path = save_report(report_md, Path(output_dir))
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
    except FeedbackParserError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqConfigurationError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqClientError as exc:
        console.print(f"[error]Groq error:[/error] {exc}")
        return 1
    except KeyboardInterrupt:
        console.print("\n[warning]Analysis cancelled.[/warning]")
        return 130


def main() -> None:
    args = parse_args()
    sys.exit(run(args.feedback_file, args.interactive, args.output_dir, args.model))


if __name__ == "__main__":
    main()

