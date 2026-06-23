from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

from competitor_parser import Competitor, parse_competitors
from groq_client import generate


console = Console()


DEFAULT_SYSTEM_PROMPT_PATH = Path("prompts/system_prompt.md")
DEFAULT_OUTPUT_PATH = Path("competitor_report.md")


def _load_system_prompt(path: Path) -> str:
    if not path.exists():
        return (
            "You are a business intelligence analyst. "
            "Analyze competitors and produce clear, actionable strategic insights."
        )
    return path.read_text(encoding="utf-8")


def build_prompt(competitors: list[Competitor]) -> str:
    competitor_lines = []
    for i, c in enumerate(competitors, start=1):
        if c.url:
            competitor_lines.append(f"{i}. {c.name} — {c.url}")
        else:
            competitor_lines.append(f"{i}. {c.name}")

    competitor_block = "\n".join(competitor_lines)

    return f"""
You are given a list of competitors. Produce a competitor monitor report.

Competitors:
{competitor_block}

Output requirements:
1) Competitor-by-competitor analysis (strengths, weaknesses, positioning)
2) Cross-competitor comparison table (feature/strategy differentiators)
3) Opportunity discovery (market gaps, white spaces, suggested positioning)
4) Strategic recommendations (growth, product, and competitive response)
5) Assumptions / uncertainties (what you could not verify)

Be concise but specific.
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent 13 — Competitor Monitor")
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to a competitors.txt file OR a comma/newline separated list of competitors.",
        default=None,
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output markdown path (default: competitor_report.md)",
    )
    args = parser.parse_args()

    system_prompt = _load_system_prompt(DEFAULT_SYSTEM_PROMPT_PATH)

    if args.input:
        input_val = args.input
        if Path(input_val).exists():
            competitors = parse_competitors(Path(input_val))
        else:
            competitors = parse_competitors(input_val.replace(",", "\n").splitlines())
    else:
        # Reasonable fallback so the agent is runnable even without an input file.
        competitors = parse_competitors([
            "Competitor A",
            "Competitor B",
            "Competitor C",
        ])

    if not competitors:
        console.print("[red]No competitors found. Provide an input file or list.[/red]")
        raise SystemExit(1)

    user_prompt = build_prompt(competitors)

    console.print("[bold green]Generating competitor report...[/bold green]")
    result = generate(system_prompt, user_prompt)

    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    header = f"# Agent 13 — Competitor Monitor\n\nGenerated (UTC): {timestamp}\n\n"
    output_path = Path(args.output)
    output_path.write_text(header + result + "\n", encoding="utf-8")

    console.print(Markdown(result))
    console.print(f"\n[bold blue]Saved report to:[/bold blue] {output_path.resolve()}")


if __name__ == "__main__":
    main()

