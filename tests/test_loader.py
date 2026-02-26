import json
import pytest
from pathlib import Path
from api_monitor.loader import load_endpoints
from api_monitor.models import Endpoint


def test_load_valid_endpoints(tmp_path):
    data = [
        {"name": "Test API", "url": "https://api.test.com", "method": "GET", "timeout": 3000}
    ]
    file = tmp_path / "endpoints.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    endpoints = load_endpoints(str(file))

    assert len(endpoints) == 1
    assert isinstance(endpoints[0], Endpoint)
    assert endpoints[0].name == "Test API"
    assert endpoints[0].url == "https://api.test.com"
    assert endpoints[0].method == "GET"
    assert endpoints[0].timeout == 3000


def test_load_endpoint_without_name(tmp_path):
    data = [{"url": "https://api.test.com"}]
    file = tmp_path / "endpoints.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    endpoints = load_endpoints(str(file))

    assert endpoints[0].name == "Endpoint 1"


def test_load_endpoint_method_uppercase(tmp_path):
    data = [{"url": "https://api.test.com", "method": "post"}]
    file = tmp_path / "endpoints.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    endpoints = load_endpoints(str(file))

    assert endpoints[0].method == "POST"


def test_load_missing_url_raises(tmp_path):
    data = [{"name": "No URL"}]
    file = tmp_path / "endpoints.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="missing required field: url"):
        load_endpoints(str(file))


def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_endpoints("non_existent.json")


def test_load_invalid_extension(tmp_path):
    file = tmp_path / "endpoints.txt"
    file.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="File must be a .json"):
        load_endpoints(str(file))


def test_load_non_list_json(tmp_path):
    file = tmp_path / "endpoints.json"
    file.write_text(json.dumps({"url": "https://api.test.com"}), encoding="utf-8")

    with pytest.raises(ValueError, match="JSON must be a list"):
        load_endpoints(str(file))