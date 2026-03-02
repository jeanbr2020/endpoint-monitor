from api_monitor.loader import load_endpoints
from api_monitor.monitor import run_monitor

def scan(filepath: str, output: str = None):
    endpoints = load_endpoints(filepath)
    results = run_monitor(endpoints)

    if output:
        from api_monitor.reporter import save_report
        save_report(results, output)

    return results