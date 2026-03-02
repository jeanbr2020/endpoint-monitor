import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch
from endpoint_monitor.models import Endpoint, CheckResult
from endpoint_monitor.reporter import generate_report, _result_to_dict


@pytest.fixture
def success_result():
    return CheckResult(
        endpoint=Endpoint(name="Test API", url="https://api.test.com", method="GET", timeout=5000),
        status_code=200,
        response_time_ms=120.5,
        success=True,
        error_message=None,
        checked_at=datetime(2026, 2, 26, 12, 0, 0)
    )


@pytest.fixture
def failure_result():
    return CheckResult(
        endpoint=Endpoint(name="Bad API", url="https://bad.test.com", method="GET", timeout=5000),
        status_code=None,
        response_time_ms=None,
        success=False,
        error_message="Connection error",
        checked_at=datetime(2026, 2, 26, 12, 0, 1)
    )


def test_result_to_dict_success(success_result):
    data = _result_to_dict(success_result)

    assert data["name"] == "Test API"
    assert data["url"] == "https://api.test.com"
    assert data["method"] == "GET"
    assert data["status_code"] == 200
    assert data["response_time_ms"] == 120.5
    assert data["success"] is True
    assert data["error_message"] is None


def test_result_to_dict_failure(failure_result):
    data = _result_to_dict(failure_result)

    assert data["success"] is False
    assert data["status_code"] is None
    assert data["response_time_ms"] is None
    assert data["error_message"] == "Connection error"


def test_save_report_creates_file(tmp_path, success_result, failure_result):
    output = tmp_path / "report.json"
    generate_report([success_result, failure_result], str(output))

    assert output.exists()


def test_save_report_summary(tmp_path, success_result, failure_result):
    output = tmp_path / "report.json"
    generate_report([success_result, failure_result], str(output))

    with open(output, encoding="utf-8") as f:
        data = json.load(f)

    assert data["summary"]["total"] == 2
    assert data["summary"]["success"] == 1
    assert data["summary"]["failed"] == 1


def test_save_report_structure(tmp_path, success_result):
    output = tmp_path / "report.json"
    generate_report([success_result], str(output))

    with open(output, encoding="utf-8") as f:
        data = json.load(f)

    assert "generated_at" in data
    assert "summary" in data
    assert "results" in data
    assert len(data["results"]) == 1


def test_generate_report_without_output(success_result):
    try:
        generate_report([success_result], None)
    except Exception as e:
        pytest.fail(f"generate_report raised unexpectedly: {e}")