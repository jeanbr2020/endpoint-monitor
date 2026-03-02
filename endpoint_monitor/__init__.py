from endpoint_monitor.loader import load_endpoints
from endpoint_monitor.monitor import run_monitor
from endpoint_monitor.reporter import save_report

def scan(filepath: str, output: str | None = None):
    endpoints = load_endpoints(filepath)
    results = run_monitor(endpoints)

    if output:
        save_report(results, output)

    return results


__all__ = ["scan"]