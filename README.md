# Endpoint Monitor

A lightweight open source CLI tool and Python library to monitor REST API endpoints, check their availability, measure response times and generate detailed reports.

> ⚠️ **Important:** This project is intended for personal use, studies and testing environments. It is **not recommended for use in production or corporate environments** without prior extensive testing. Do not use this tool with endpoints that handle sensitive data without fully understanding the risks involved. The developer is not responsible for any damage, data loss or unexpected behavior resulting from the use or modification of this software. See the [LICENSE](LICENSE) for more details.

---

## Features

- Monitor multiple endpoints from a JSON file
- Supports GET, POST, PUT, DELETE and other HTTP methods
- Real-time progress bar in the terminal
- Formatted table output with status, response time and result
- Optional JSON report export
- Safe file handling — prompts before overwriting existing report files
- Clear error messages for timeouts and connection failures
- Can be used as a CLI tool or imported as a Python library

---

## Requirements

- Python 3.10+

---

## Installation

```bash
pip install endpoint-monitor
```

---

## Usage

### CLI

#### Basic — display results in terminal

```bash
endpoint-monitor endpoints.json
```

#### Save report to JSON file

```bash
endpoint-monitor endpoints.json --output report.json
endpoint-monitor endpoints.json -o report.json
```

#### Help

```bash
endpoint-monitor --help
```

---

### Python Library

You can also import and use `endpoint-monitor` directly in your Python projects:

```python
from api_monitor import scan

# Run monitor and get results
results = scan("endpoints.json")

# Run monitor and save JSON report
results = scan("endpoints.json", output="report.json")
```

Each result in the list contains:

| Field | Type | Description |
|---|---|---|
| `endpoint.name` | string | Endpoint display name |
| `endpoint.url` | string | Endpoint URL |
| `endpoint.method` | string | HTTP method |
| `status_code` | int or None | HTTP response status code |
| `response_time_ms` | float or None | Response time in milliseconds |
| `success` | bool | Whether the request succeeded |
| `error_message` | string or None | Error description if failed |
| `checked_at` | datetime | Timestamp of the check |

---

## Safe file handling

When using `--output` and the specified file already exists, the tool will prompt you with the following options:

```
⚠️  Warning: 'report.json' already exists in the current directory.
What do you want to do?
  [r] Rename
  [o] Overwrite
  [c] Cancel
```

If you choose **Rename**, you will be asked for a new filename. If the new name also exists, the tool will ask again until a unique name is provided.

If you choose **Overwrite**, a confirmation prompt will appear before proceeding:

```
⚠️  Are you sure you want to overwrite 'report.json'? This action cannot be undone.
  [y] Yes, overwrite
  [b] Back to options
```

If you choose **Cancel**, no file will be saved and the operation is aborted safely.

Any input other than the listed options will be rejected and the prompt will repeat.

---

## How to pass your endpoints file

The `FILE` argument is the path to your JSON file on your system.
You do not need to be in the same folder as the file — just pass the correct path.

**File in the current folder:**
```bash
endpoint-monitor endpoints.json
```

**File in another folder (Linux/Mac):**
```bash
endpoint-monitor ~/Documents/endpoints.json
endpoint-monitor /home/yourname/projects/endpoints.json
```

**File in another folder (Windows):**
```bash
endpoint-monitor C:\Users\YourName\Documents\endpoints.json
```

**Tip:** The easiest way is to navigate to the folder where your file is and run the command from there.
```bash
cd C:\Users\YourName\Documents
endpoint-monitor endpoints.json
```

---

## Endpoint file format

Create a `.json` file with a list of endpoints. Only `url` is required — all other fields are optional.

```json
[
  {
    "name": "GitHub API",
    "url": "https://api.github.com",
    "method": "GET",
    "timeout": 5000
  },
  {
    "name": "My API",
    "url": "https://myapi.com/health",
    "method": "GET",
    "timeout": 3000
  }
]
```

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `url` | string | ✓ | — | Endpoint URL |
| `name` | string | ✗ | `Endpoint N` | Display name |
| `method` | string | ✗ | `GET` | HTTP method |
| `timeout` | int | ✗ | `5000` | Timeout in milliseconds |

---

## Report output example

```
╭───────────────────┬────────┬────────┬───────────────┬────────────────────╮
│ Endpoint          │ Method │ Status │ Response Time │       Result       │
├───────────────────┼────────┼────────┼───────────────┼────────────────────┤
│ GitHub API        │  GET   │  200   │         482ms │        ✓ OK        │
│ My API            │  GET   │  200   │         310ms │        ✓ OK        │
│ Broken Endpoint   │  GET   │   —    │             — │ ✗ Connection error │
╰───────────────────┴────────┴────────┴───────────────┴────────────────────╯

Total: 3  Success: 2  Failed: 1
```

---

## Project structure

```
api_monitor/
├── __init__.py   # Public library interface
├── cli.py        # CLI entry point
├── monitor.py    # Orchestrates the monitoring flow
├── checker.py    # Performs HTTP requests and returns results
├── loader.py     # Reads and validates the JSON file
├── reporter.py   # Generates terminal output and JSON report
└── models.py     # Data models
```

---

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Changelog

### v0.2.0
- Added public `scan()` function — `endpoint-monitor` can now be used as a Python library
- Added safe file handling for JSON report export — prompts to rename, overwrite or cancel when file already exists
- Added input validation on all prompts — invalid options are rejected and the prompt repeats

### v0.1.0
- Initial release

---

## Open Source

This project is open source and contributions are welcome. If you find a bug or have a suggestion, feel free to open an issue or submit a pull request.

If you wish to modify or distribute this software, please read the [LICENSE](LICENSE) carefully. The developer provides no warranties and takes no responsibility for any damages arising from the use or modification of this project.

---

## License

MIT License — see [LICENSE](LICENSE) for details.