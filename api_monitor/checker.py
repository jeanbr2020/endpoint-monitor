import requests
from datetime import datetime
from api_monitor.models import Endpoint, CheckResult


def check_endpoint(endpoint: Endpoint) -> CheckResult:
    checked_at = datetime.now()

    try:
        response = _make_request(endpoint)
        return CheckResult(
            endpoint=endpoint,
            status_code=response.status_code,
            response_time_ms=response.elapsed.total_seconds() * 1000,
            success=_is_success(response.status_code),
            error_message=None,
            checked_at=checked_at
        )

    except requests.Timeout:
        return _failure(endpoint, checked_at, "Request timed out")

    except requests.ConnectionError:
        return _failure(endpoint, checked_at, "Connection error")

    except requests.RequestException as e:
        return _failure(endpoint, checked_at, str(e))


def _make_request(endpoint: Endpoint) -> requests.Response:
    return requests.request(
        method=endpoint.method,
        url=endpoint.url,
        timeout=endpoint.timeout / 1000
    )


def _is_success(status_code: int) -> bool:
    return 200 <= status_code < 300


def _failure(endpoint: Endpoint, checked_at: datetime, error: str) -> CheckResult:
    return CheckResult(
        endpoint=endpoint,
        status_code=None,
        response_time_ms=None,
        success=False,
        error_message=error,
        checked_at=checked_at
    )