from dataclasses import dataclass
from datetime import datetime

@dataclass
class Endpoint:
    name: str
    url: str
    method: str = "GET"
    timeout: int = 5000

@dataclass
class CheckResult:
    endpoint: Endpoint
    status_code: int | None
    response_time_ms: float | None
    success: bool
    error_message: str | None
    checked_at: datetime