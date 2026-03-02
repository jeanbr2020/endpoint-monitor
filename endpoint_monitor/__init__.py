from endpoint_monitor.loader import load_endpoints
from endpoint_monitor.monitor import run_monitor

def scan(filepath: str, output: str | None = None):
    endpoints = load_endpoints(filepath)
    results = run_monitor(endpoints)

    if output:
        from endpoint_monitor.reporter import save_report
        save_report(results, output)

    return results


__all__ = ["scan"]