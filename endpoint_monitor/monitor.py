from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from endpoint_monitor.models import Endpoint, CheckResult
from endpoint_monitor.checker import check_endpoint


def run_monitor(endpoints: list[Endpoint]) -> list[CheckResult]:
    results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
    ) as progress:

        task = progress.add_task("Checking endpoints...", total=len(endpoints))

        for endpoint in endpoints:
            progress.update(task, description=f"Checking {endpoint.name}")
            result = check_endpoint(endpoint)
            results.append(result)
            progress.advance(task)

    return results