"""Repo Explainer Agent — CLI entry point."""

from __future__ import annotations

import argparse
import os
import re
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.theme import Theme

from github_client import (
    GitHubClient,
    GitHubClientError,
    InvalidRepoURLError,
    RepositoryNotFoundError,
    build_repo_context,
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
    }
)
console = Console(theme=THEME)

SECTION_ORDER = [
    "Project Summary",
    "Tech Stack",
    "Architecture Overview",
    "Key Files",
    "Folder Structure Explanation",
    "Improvement Suggestions",
]

SECTION_ALIASES = {
    "Recommendations": "Improvement Suggestions",
    "Recommendation": "Improvement Suggestions",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a GitHub repository and explain it in simple language.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="GitHub repository URL (example: https://github.com/user/project)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        help="Groq model to use for analysis",
    )
    return parser.parse_args()


def prompt_for_url() -> str:
    console.print("[info]Enter a public GitHub repository URL.[/info]")
    return console.input("[bold]Repository URL:[/bold] ").strip()


def split_analysis_sections(analysis: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(analysis))
    if not matches:
        return [("Analysis", analysis.strip())]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        title = SECTION_ALIASES.get(title, title)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(analysis)
        body = analysis[start:end].strip()
        sections.append((title, body))
    return sections


def display_header(owner: str, repo: str) -> None:
    console.print()
    console.print(
        Panel.fit(
            f"[title]Repo Explainer[/title]\n[info]Analyzing[/info] [bold]{owner}/{repo}[/bold]",
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


def run(url: str, model: str) -> int:
    if not url:
        url = prompt_for_url()
    if not url:
        console.print("[error]No repository URL provided.[/error]")
        return 1

    github_token = os.getenv("GITHUB_TOKEN")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Fetching repository data from GitHub...", total=None)
            github = GitHubClient(token=github_token)
            repo_data = github.fetch_repository(url)

        display_header(repo_data.owner, repo_data.repo)
        repo_context = build_repo_context(repo_data)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Generating structured analysis with Groq...", total=None)
            groq = GroqClient(model=model)
            analysis = groq.analyze_repository(repo_context)

        sections = split_analysis_sections(analysis)
        display_sections(sections)

        console.print(
            Panel(
                "[success]Analysis complete.[/success] Review the sections above for a structured repository overview.",
                border_style="green",
            )
        )
        return 0

    except InvalidRepoURLError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except RepositoryNotFoundError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GroqConfigurationError as exc:
        console.print(f"[error]{exc}[/error]")
        return 1
    except GitHubClientError as exc:
        console.print(f"[error]GitHub error:[/error] {exc}")
        return 1
    except GroqClientError as exc:
        console.print(f"[error]Groq error:[/error] {exc}")
        return 1
    except KeyboardInterrupt:
        console.print("\n[warning]Analysis cancelled.[/warning]")
        return 130


def main() -> None:
    args = parse_args()
    sys.exit(run(args.url, args.model))


if __name__ == "__main__":
    main()
