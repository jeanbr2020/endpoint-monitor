import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from endpoint_monitor.models import CheckResult

console = Console()


def generate_report(results: list[CheckResult], output_path: str | None = None) -> None:
    _print_table(results)
    _print_summary(results)

    if output_path:
        path = Path(output_path)
        if path.exists():
            resolved_path = _handle_existing_file(path)
            if resolved_path is None:
                console.print("\n[yellow]✗ Operation cancelled. No file was saved.[/yellow]\n")
                return
            _save_report(results, str(resolved_path))
        else:
            _save_report(results, output_path)


def _handle_existing_file(path: Path) -> Path | None:
    while True:
        console.print(f"\n[yellow]⚠️  Warning:[/yellow] '[cyan]{path.name}[/cyan]' already exists in the current directory.")
        console.print("What do you want to do?")
        console.print("  [r] Rename", markup=False)
        console.print("  [o] Overwrite", markup=False)
        console.print("  [c] Cancel\n", markup=False)

        choice = console.input("Choice: ").strip().lower()

        if choice == "r":
            return _handle_rename(path)
        elif choice == "o":
            return _handle_overwrite(path)
        elif choice == "c":
            return None
        else:
            console.print("\n✗ Invalid option. Please choose [r], [o] or [c].", markup=False)


def _handle_rename(path: Path) -> Path | None:
    while True:
        new_name = console.input("New name: ").strip()

        if not new_name:
            console.print("[red]✗ Name cannot be empty.[/red]")
            continue

        new_path = path.parent / new_name

        if new_path.exists():
            console.print(f"[red]✗ '{new_name}' already exists. Please choose a different name.[/red]")
            continue

        return new_path


def _handle_overwrite(path: Path) -> Path | None:
    while True:
        console.print(f"\n[yellow]⚠️  Are you sure you want to overwrite '[cyan]{path.name}[/cyan]'? This action cannot be undone.[/yellow]")
        console.print("  [y] Yes, overwrite", markup=False)
        console.print("  [b] Back to options\n", markup=False)

        choice = console.input("Choice: ").strip().lower()

        if choice == "y":
            return path
        elif choice == "b":
            return _handle_existing_file(path)
        else:
            console.print("✗ Invalid option. Please choose [y] or [b].", markup=False)


def _print_table(results: list[CheckResult]) -> None:
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold white")
    table.add_column("Endpoint", style="cyan")
    table.add_column("Method", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Response Time", justify="right")
    table.add_column("Result", justify="center")

    for result in results:
        table.add_row(
            result.endpoint.name,
            result.endpoint.method,
            str(result.status_code) if result.status_code else "—",
            f"{result.response_time_ms:.0f}ms" if result.response_time_ms else "—",
            "[green]✓ OK[/green]" if result.success else f"[red]✗ {result.error_message}[/red]"
        )

    console.print(table)


def _print_summary(results: list[CheckResult]) -> None:
    total = len(results)
    success = sum(1 for r in results if r.success)
    failed = total - success

    console.print(f"\n[bold]Total:[/bold] {total}  "
                  f"[green]Success: {success}[/green]  "
                  f"[red]Failed: {failed}[/red]\n")


def _save_report(results: list[CheckResult], output_path: str) -> None:
    path = Path(output_path)
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total": len(results),
            "success": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success)
        },
        "results": [_result_to_dict(r) for r in results]
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    console.print(f"\n[green]✓ Report saved as '{path.name}'[/green]\n")


def _result_to_dict(result: CheckResult) -> dict:
    return {
        "name": result.endpoint.name,
        "url": result.endpoint.url,
        "method": result.endpoint.method,
        "status_code": result.status_code,
        "response_time_ms": round(result.response_time_ms, 2) if result.response_time_ms else None,
        "success": result.success,
        "error_message": result.error_message,
        "checked_at": result.checked_at.isoformat()
    }