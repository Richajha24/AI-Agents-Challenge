"""AI Recruiter Agent — CLI entry point."""

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

from groq_client import GroqClient, GroqClientError, GroqConfigurationError
from resume_parser import (
    EmptyInputError,
    EvaluationInput,
    InvalidPathError,
    PdfParseError,
    ResumeParserError,
    UnsupportedFileTypeError,
    build_evaluation_context,
    read_job_from_file,
    read_job_from_text,
    read_resume_from_file,
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
        "strong_hire": "bold green",
        "hire": "green",
        "maybe": "yellow",
        "no_hire": "bold red",
    }
)
console = Console(theme=THEME, force_terminal=True)

SECTION_ORDER = [
    "Resume Extraction",
    "Match Score",
    "Skills Analysis",
    "Missing Skills",
    "Candidate Strengths",
    "Candidate Weaknesses",
    "Interview Recommendation",
    "Improvement Suggestions",
]

OUTPUT_FILENAME = "hiring_report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a candidate resume against a job description and generate hiring recommendations.",
    )
    parser.add_argument(
        "-r",
        "--resume",
        dest="resume_path",
        help="Path to resume file (PDF, .txt, or .md)",
    )
    parser.add_argument(
        "-j",
        "--job",
        dest="job_text",
        help="Job description text",
    )
    parser.add_argument(
        "-f",
        "--job-file",
        dest="job_file_path",
        help="Path to a text file containing the job description",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where hiring_report.md will be saved (default: current directory)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        help="Groq model to use for analysis",
    )
    return parser.parse_args()


def prompt_for_resume_path() -> str:
    console.print("[info]Enter the path to the candidate resume (PDF or text file).[/info]")
    return console.input("[bold]Resume path:[/bold] ").strip()


def prompt_for_job_description() -> str:
    console.print(
        "[info]Enter the job description below. "
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


def load_evaluation(resume_path: str | None, job_text: str | None, job_file_path: str | None) -> EvaluationInput:
    resolved_resume = resume_path or prompt_for_resume_path()
    if not resolved_resume:
        raise EmptyInputError("No resume path provided.")

    resume = read_resume_from_file(Path(resolved_resume))

    if job_file_path:
        job = read_job_from_file(Path(job_file_path))
    elif job_text:
        job = read_job_from_text(job_text, source="command line argument")
    else:
        text = prompt_for_job_description()
        job = read_job_from_text(text, source="interactive input")

    return EvaluationInput(resume=resume, job_description=job)


def split_report_sections(report: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(report))
    if not matches:
        return [("Hiring Report", report.strip())]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        body = report[start:end].strip()
        sections.append((title, body))
    return sections


def parse_match_score(body: str) -> int | None:
    match = re.search(r"Match Score:\s*(\d{1,3})\s*/\s*100", body, re.IGNORECASE)
    if not match:
        return None
    return min(100, max(0, int(match.group(1))))


def score_bar(value: int, width: int = 30) -> str:
    filled = int(value / 100 * width)
    return "#" * filled + "-" * (width - filled)


def parse_recommendation(body: str) -> str | None:
    for label in ("Strong Hire", "Hire", "Maybe", "No Hire"):
        if re.search(rf"\*\*{re.escape(label)}\*\*|{re.escape(label)}", body, re.IGNORECASE):
            return label
    return None


def recommendation_style(label: str | None) -> str:
    if not label:
        return "info"
    normalized = label.lower()
    if normalized == "strong hire":
        return "strong_hire"
    if normalized == "hire":
        return "hire"
    if normalized == "maybe":
        return "maybe"
    return "no_hire"


def recommendation_border_style(label: str | None) -> str:
    if not label:
        return "cyan"
    normalized = label.lower()
    if normalized in {"strong hire", "hire"}:
        return "green"
    if normalized == "maybe":
        return "yellow"
    return "red"


def display_header(evaluation: EvaluationInput) -> None:
    job_preview = evaluation.job_description.content.replace("\n", " ")
    if len(job_preview) > 100:
        job_preview = job_preview[:97] + "..."

    console.print()
    console.print(
        Panel.fit(
            f"[title]AI Recruiter[/title]\n"
            f"[info]Resume:[/info] [bold]{evaluation.resume.source}[/bold] "
            f"([info]{evaluation.resume.file_type}[/info])\n"
            f"[info]Job Description:[/info] {evaluation.job_description.source}\n"
            f"[info]Preview:[/info] {job_preview}",
            border_style="magenta",
        )
    )
    console.print()


def display_match_score(body: str) -> None:
    score = parse_match_score(body)
    if score is None:
        console.print(Markdown(body))
        console.print()
        return

    color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Label", style="cyan")
    table.add_column("Value")
    table.add_row("Match Score", f"[{color} bold]{score}/100[/{color} bold]")
    table.add_row("Visual", f"[{color}]{score_bar(score)}[/{color}]")
    console.print(table)
    console.print()

    rationale = re.sub(r"Match Score:\s*\d{1,3}\s*/\s*100\s*", "", body, flags=re.IGNORECASE).strip()
    if rationale:
        console.print(Markdown(rationale))
        console.print()


def display_interview_recommendation(body: str) -> None:
    recommendation = parse_recommendation(body)
    if recommendation:
        style = recommendation_style(recommendation)
        console.print(
            Panel(
                f"[{style}]{recommendation}[/{style}]",
                title="Recommendation",
                border_style=recommendation_border_style(recommendation),
            )
        )
        console.print()
    console.print(Markdown(body))
    console.print()


def display_section(title: str, body: str) -> None:
    console.print(Rule(f"[title]{title}[/title]", style="magenta"))

    if title == "Match Score":
        display_match_score(body)
    elif title == "Interview Recommendation":
        display_interview_recommendation(body)
    else:
        console.print(Markdown(body))
        console.print()


def display_sections(sections: list[tuple[str, str]]) -> None:
    section_map = dict(sections)
    ordered_titles = [title for title in SECTION_ORDER if title in section_map]
    remaining = [title for title, _ in sections if title not in ordered_titles]

    for title in ordered_titles + remaining:
        display_section(title, section_map[title])


def save_report(report: str, output_dir: Path) -> Path:
    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(report.strip() + "\n", encoding="utf-8")
    return output_path


def run(
    resume_path: str | None,
    job_text: str | None,
    job_file_path: str | None,
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
            progress.add_task("Reading resume and job description...", total=None)
            evaluation = load_evaluation(resume_path, job_text, job_file_path)

        display_header(evaluation)
        context = build_evaluation_context(evaluation)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Generating hiring report with Groq...", total=None)
            groq = GroqClient(model=model)
            report = groq.analyze_candidate(context)

        sections = split_report_sections(report)
        display_sections(sections)

        output_path = save_report(report, Path(output_dir))
        console.print(
            Panel(
                f"[success]Hiring report saved to[/success] [bold]{output_path.resolve()}[/bold]",
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
    except ResumeParserError as exc:
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
    sys.exit(run(args.resume_path, args.job_text, args.job_file_path, args.output_dir, args.model))


if __name__ == "__main__":
    main()
