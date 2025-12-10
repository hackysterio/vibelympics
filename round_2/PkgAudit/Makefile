.PHONY: build run test docker docker-run clean lint

PYTHON := python3
PIP := pip3
PORT := 8080

build:
	$(PIP) install -r requirements.txt

run:
	cd src && $(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port $(PORT) --reload

test:
	$(PYTHON) -m pytest tests/ -v --tb=short

test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing

docker:
	docker build -t pkgaudit .

docker-run:
	docker run --rm -p $(PORT):$(PORT) pkgaudit

docker-dev:
	docker build -t pkgaudit . && docker run --rm -p $(PORT):$(PORT) pkgaudit

cli:
	cd src && $(PYTHON) cli.py $(PKG)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "cache.db" -delete 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	rm -rf htmlcov 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true

lint:
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=120

help:
	@echo "PkgAudit - npm Package Security Auditor"
	@echo ""
	@echo "Available targets:"
	@echo "  build       - Install Python dependencies"
	@echo "  run         - Run the web application locally"
	@echo "  test        - Run pytest test suite"
	@echo "  test-cov    - Run tests with coverage report"
	@echo "  docker      - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  cli PKG=x   - Run CLI audit for package x"
	@echo "  clean       - Remove cache and temp files"
	@echo "  lint        - Run flake8 linter"
	@echo ""
	@echo "Examples:"
	@echo "  make run"
	@echo "  make cli PKG=express"
	@echo "  make docker && make docker-run"
