import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from api_monitor.models import CheckResult


console = Console()


def generate_report(results: list[CheckResult], output_path: str | None = None) -> None:
    _print_table(results)
    _print_summary(results)

    if output_path:
        _save_report(results, output_path)


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

    console.print(f"[dim]Report saved to {output_path}[/dim]")


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