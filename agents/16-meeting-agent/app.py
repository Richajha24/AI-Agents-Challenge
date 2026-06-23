import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from groq_client import GroqClient

console = Console()


def load_system_prompt() -> str:
    """Load the system prompt from the prompts directory."""
    prompt_path = Path(__file__).parent / "prompts" / "system_prompt.md"
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        console.print("[red]Error: system_prompt.md not found in prompts directory[/red]")
        sys.exit(1)


def load_meeting_context(file_path: str = None) -> str:
    """
    Load meeting context from a file or get it from user input.
    
    Args:
        file_path: Optional path to a file containing meeting context
        
    Returns:
        The meeting context as a string
    """
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            console.print(f"[red]Error: File '{file_path}' not found[/red]")
            sys.exit(1)
    else:
        console.print("\n[bold cyan]Enter your meeting context (press Enter twice to finish):[/bold cyan]")
        console.print("[dim]Example: Weekly team sync to discuss Q4 product roadmap and resource allocation[/dim]\n")
        
        lines = []
        while True:
            line = input()
            if line == "" and len(lines) > 0 and lines[-1] == "":
                break
            lines.append(line)
        
        return "\n".join(lines).strip()


def save_meeting_report(content: str, output_file: str = "meeting_report.md"):
    """
    Save the generated meeting report to a file.
    
    Args:
        content: The meeting report content
        output_file: The output file path
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"\n[green]✓ Meeting report saved to {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving report: {str(e)}[/red]")


def main():
    """Main entry point for the Meeting Agent."""
    console.print(Panel.fit(
        "[bold cyan]Meeting Agent[/bold cyan]\n[dim]AI-powered meeting materials generator[/dim]",
        border_style="cyan"
    ))
    
    try:
        # Load system prompt
        system_prompt = load_system_prompt()
        
        # Get meeting context
        file_path = sys.argv[1] if len(sys.argv) > 1 else None
        meeting_context = load_meeting_context(file_path)
        
        if not meeting_context:
            console.print("[red]Error: Meeting context cannot be empty[/red]")
            sys.exit(1)
        
        # Initialize Groq client
        console.print("\n[bold yellow]Initializing Groq client...[/bold yellow]")
        groq_client = GroqClient()
        
        # Generate meeting materials
        console.print("[bold yellow]Generating meeting materials...[/bold yellow]")
        meeting_materials = groq_client.generate_meeting_materials(meeting_context, system_prompt)
        
        # Display the results
        console.print("\n[bold green]Generated Meeting Materials:[/bold green]\n")
        console.print(Panel(
            Markdown(meeting_materials),
            border_style="green",
            padding=(1, 2)
        ))
        
        # Save to file
        save_meeting_report(meeting_materials)
        
        console.print("\n[bold cyan]✓ Meeting Agent completed successfully![/bold cyan]\n")
        
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print("[dim]Please ensure GROQ_API_KEY is set in your .env file[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()