from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from api_monitor.loader import load_endpoints
from api_monitor.monitor import run_monitor
from api_monitor.reporter import generate_report


app = typer.Typer(
    name="api-monitor",
    help="A CLI tool to monitor REST API endpoints."
)

console = Console()


@app.command()
def run(
    file: Path = typer.Argument(
        ...,
        help=(
            "Path to the JSON file containing the endpoints. "
            "Examples: 'api-monitor endpoints.json' if the file is in the current folder, "
            "'api-monitor ~/Documents/endpoints.json' for a file in another folder, "
            "or 'api-monitor C:\\Users\\YourName\\endpoints.json' on Windows."
        ),
        exists=True,
        readable=True
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Path to save the report as a JSON file. Example: --output report.json"
    )
):
    """
    Monitor all endpoints defined in a JSON file.

    The FILE argument must be the path to your endpoints JSON file.
    The file can be in the current directory or anywhere on your system.

    Examples:\n
        api-monitor endpoints.json\n
        api-monitor ~/Documents/endpoints.json\n
        api-monitor C:\\\\Users\\\\YourName\\\\endpoints.json\n
        api-monitor endpoints.json --output report.json
    """
    try:
        endpoints = load_endpoints(str(file))
        console.print(f"\n[bold]Found {len(endpoints)} endpoint(s). Starting monitor...[/bold]\n")

        results = run_monitor(endpoints)
        generate_report(results, str(output) if output else None)

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    except ValueError as e:
        console.print(f"[red]Invalid file:[/red] {e}")
        raise typer.Exit(code=1)


def main():
    app()