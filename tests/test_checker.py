import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from endpoint_monitor.checker import check_endpoint, _is_success
from endpoint_monitor.models import Endpoint, CheckResult
import requests


@pytest.fixture
def endpoint():
    return Endpoint(
        name="Test API",
        url="https://api.test.com",
        method="GET",
        timeout=5000
    )


def test_check_success(endpoint):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed.total_seconds.return_value = 0.3

    with patch("api_monitor.checker.requests.request", return_value=mock_response):
        result = check_endpoint(endpoint)

    assert result.success is True
    assert result.status_code == 200
    assert result.response_time_ms == 300.0
    assert result.error_message is None


def test_check_server_error(endpoint):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.elapsed.total_seconds.return_value = 0.1

    with patch("api_monitor.checker.requests.request", return_value=mock_response):
        result = check_endpoint(endpoint)

    assert result.success is False
    assert result.status_code == 500


def test_check_timeout(endpoint):
    with patch("api_monitor.checker.requests.request", side_effect=requests.Timeout):
        result = check_endpoint(endpoint)

    assert result.success is False
    assert result.status_code is None
    assert result.error_message == "Request timed out"


def test_check_connection_error(endpoint):
    with patch("api_monitor.checker.requests.request", side_effect=requests.ConnectionError):
        result = check_endpoint(endpoint)

    assert result.success is False
    assert result.status_code is None
    assert result.error_message == "Connection error"


def test_check_returns_check_result(endpoint):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed.total_seconds.return_value = 0.2

    with patch("api_monitor.checker.requests.request", return_value=mock_response):
        result = check_endpoint(endpoint)

    assert isinstance(result, CheckResult)
    assert isinstance(result.checked_at, datetime)


def test_is_success_valid_codes():
    assert _is_success(200) is True
    assert _is_success(201) is True
    assert _is_success(299) is True


def test_is_success_invalid_codes():
    assert _is_success(300) is False
    assert _is_success(404) is False
    assert _is_success(500) is False