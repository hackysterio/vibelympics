# PkgAudit - npm Package Ecosystem Auditor

A comprehensive security auditing tool for npm packages that analyzes supply chain risks, detects typosquatting attempts, and performs static code analysis.

![Risk Score Demo](docs/demo-placeholder.png)

## Features

- **Typosquatting Detection**: Compares package names against 80+ popular npm packages using Levenshtein distance
- **Maintainer Analysis**: Evaluates maintainer count, email domains, and GitHub presence
- **Publish Activity Monitoring**: Detects suspicious release patterns including dormant-then-sudden releases
- **Dependency Analysis**: Flags high dependency counts and deprecated packages
- **Static Tarball Scanning**: Analyzes package code for dangerous patterns without execution
- **Visual Risk Reports**: Color-coded risk meters and detailed breakdowns

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web application
cd src && python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# Or use Make
make build
make run
```

### Docker

```bash
# Build the image
docker build -t pkgaudit .

# Run the container
docker run --rm -p 8080:8080 pkgaudit
```

### CLI Usage

```bash
# Audit a package via command line
cd src && python cli.py express

# Output: JSON report to stdout
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI with search form |
| `/health` | GET | Health check (returns 200 OK) |
| `/api/audit?pkg=<name>` | GET | Returns JSON audit report |
| `/audit` | POST | Form submission, returns HTML report |
| `/api/report/<name>.json` | GET | Returns cached report if available |

## How Risk is Computed

The final risk score (0-100) is calculated using weighted subscores:

### Subscores (0-100 each)

**Publish Activity (weight: 0.25)**
- 5+ releases in 7 days → 90
- 2+ releases in 7 days → 65
- Dormant (>365 days) then sudden release (≤7 days) → 80
- Otherwise → 10

**Maintainer (weight: 0.20)**
- Base: 0
- Single maintainer: +70
- Recently added maintainer (<30 days): +20
- Missing GitHub repository: +20
- Free email domain (gmail, yahoo, etc.): +10
- Maximum: 100

**Dependencies (weight: 0.20)**
- >50 dependencies → 90
- >20 dependencies → 60
- >5 dependencies → 30
- +15 per deprecated dependency (capped at 100)
- +10 per dependency missing repository (capped at 100)

**Typosquatting (weight: 0.15)**
- Levenshtein distance 1 & unpopular package → 90
- Levenshtein distance 1 & popular package → 60
- Levenshtein distance 2 → 30
- Otherwise → 0

**Tarball Scan (weight: 0.20)**
- postinstall/preinstall scripts: +60
- Network commands (curl/wget/nc): +50
- eval()/Function() calls: +40
- High-entropy strings (>4.0 entropy, >100 chars): +50
- Maximum: 100

### Final Score

```
risk_score = round(
    publish_activity * 0.25 +
    maintainer * 0.20 +
    dependency * 0.20 +
    typosquat * 0.15 +
    tarball_scan * 0.20
)
```

### Severity Levels

- **Low**: 0-30
- **Medium**: 31-60
- **High**: 61-100

## Output JSON Schema

```json
{
  "package": "<name>",
  "version": "<latest>",
  "risk_score": 45,
  "severity": "Medium",
  "risk_breakdown": {
    "publish_activity": 10,
    "maintainer": 70,
    "dependency": 30,
    "typosquat": 0,
    "tarball_scan": 60
  },
  "flags": [
    "Single maintainer",
    "Contains postinstall scripts"
  ],
  "evidence": {
    "maintainers": [...],
    "latest_release_date": "2024-01-15T10:30:00Z",
    "tarball_findings": [...],
    "publish_timeline": [...]
  },
  "timestamp": "2024-12-10T12:00:00Z"
}
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
python -m pytest tests/test_audit.py -v
```

## Project Structure

```
pkgaudit/
├── src/
│   ├── main.py              # FastAPI application
│   ├── audit.py             # Core scoring & helpers
│   ├── registry.py          # npm API wrapper & caching
│   ├── tarball_scanner.py   # Static code analysis
│   ├── cli.py               # Command-line interface
│   ├── templates/
│   │   ├── index.html       # Search page
│   │   └── report.html      # Audit report page
│   └── static/
│       └── styles.css       # Stylesheet
├── tests/
│   ├── test_audit.py        # Unit tests
│   └── test_integration.py  # Integration tests
├── sample_reports/          # Pre-generated example reports
├── Dockerfile
├── Makefile
├── requirements.txt
└── README.md
```

## Security Notes

- **No Code Execution**: The tarball scanner performs static analysis only. No downloaded JavaScript is ever executed.
- **Safe Extraction**: Tarball extraction uses path validation to prevent directory traversal attacks.
- **Caching**: Results are cached for 24 hours in a local SQLite database to reduce API calls.

## License

MIT License

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting a pull request.

---

Built for the Vibelympics Hackathon - Software Supply Chain Security Challenge
