# Endpoint Monitor

A lightweight open source CLI tool to monitor REST API endpoints, check their availability, measure response times and generate detailed reports.

> ⚠️ **Important:** This project is intended for personal use, studies and testing environments. It is **not recommended for use in production or corporate environments** without prior extensive testing. Do not use this tool with endpoints that handle sensitive data without fully understanding the risks involved. The developer is not responsible for any damage, data loss or unexpected behavior resulting from the use or modification of this software. See the [LICENSE](LICENSE) for more details.

---

## Features

- Monitor multiple endpoints from a JSON file
- Supports GET, POST, PUT, DELETE and other HTTP methods
- Real-time progress bar in the terminal
- Formatted table output with status, response time and result
- Optional JSON report export
- Clear error messages for timeouts and connection failures

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

### Basic — display results in terminal

```bash
endpoint-monitor endpoints.json
```

### Save report to JSON file

```bash
endpoint-monitor endpoints.json --output report.json
endpoint-monitor endpoints.json -o report.json
```

### Help

```bash
endpoint-monitor --help
```

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

## Open Source

This project is open source and contributions are welcome. If you find a bug or have a suggestion, feel free to open an issue or submit a pull request.

If you wish to modify or distribute this software, please read the [LICENSE](LICENSE) carefully. The developer provides no warranties and takes no responsibility for any damages arising from the use or modification of this project.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
