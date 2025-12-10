# PkgAudit - npm Package Ecosystem Auditor

## Overview
PkgAudit is a comprehensive security auditing tool for npm packages that analyzes supply chain risks. It was built for the Vibelympics Hackathon (Challenge 2: Package Ecosystem Auditor) focusing on software supply chain security.

## Current State
- Fully functional web application with FastAPI backend
- Complete audit pipeline: registry parsing, typosquatting detection, maintainer analysis, dependency analysis, tarball scanning
- Visual HTML reports with risk meters and sparkline charts
- JSON API endpoints for programmatic access
- CLI tool for command-line audits
- SQLite caching with 24-hour TTL
- Docker support with health checks
- Comprehensive pytest test suite

## Project Architecture

### Directory Structure
```
/src
  main.py           - FastAPI application with all routes
  audit.py          - Core scoring algorithms, Levenshtein, entropy
  registry.py       - npm API wrapper with SQLite caching
  tarball_scanner.py - Static code analysis for tarballs
  cli.py            - Command-line interface
  /templates
    index.html      - Search page
    report.html     - Audit report page
  /static
    styles.css      - All styling

/tests
  test_audit.py     - Unit tests for scoring functions
  test_integration.py - Integration tests with mocked registry

/sample_reports     - Pre-generated example JSON reports
/.github/workflows  - CI configuration
```

### Key Technologies
- **Backend**: Python 3.11, FastAPI, uvicorn
- **HTTP Client**: httpx (async)
- **Templates**: Jinja2
- **Testing**: pytest, pytest-asyncio
- **Caching**: SQLite
- **Container**: Docker with python:3.11-slim

### Risk Scoring Algorithm
Final score = weighted sum of 5 subscores:
- publish_activity (25%): Detects unusual release patterns
- maintainer (20%): Evaluates maintainer trust signals
- dependency (20%): Counts and analyzes dependencies
- typosquat (15%): Levenshtein distance to popular packages
- tarball_scan (20%): Static analysis for dangerous patterns

### API Endpoints
- `GET /` - Web UI
- `GET /health` - Health check
- `GET /api/audit?pkg=<name>` - JSON audit
- `POST /audit` - Form submission (HTML response)
- `GET /api/report/<name>.json` - Cached report

## Running the Application
- Web app runs on port 5000 (development) or 8080 (Docker)
- Start: `cd src && python -m uvicorn main:app --host 0.0.0.0 --port 5000`
- CLI: `cd src && python cli.py express`

## User Preferences
- No preferences recorded yet

## Recent Changes
- 2024-12-10: Initial project creation with all core features
