import json
from pathlib import Path
from endpoint_monitor.models import Endpoint

def load_endpoints(file_path: str) -> list[Endpoint]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.suffix == ".json":
        raise ValueError("File must be a .json")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON must be a list of endpoints")
    
    return [_parse_endpoint(item, index) for index, item in enumerate(data)]

def _parse_endpoint(item: dict, index: int) -> Endpoint:
    if "url" not in item:
        raise ValueError(f"Endpoint at index {index} is missing required field: url")
    
    return Endpoint(
        name=item.get("name", f"Endpoint {index + 1}"),
        url=item["url"],
        method=item.get("method", "GET").upper(),
        timeout=item.get("timeout", 5000)
    )
