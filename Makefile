PYTHON := $(or \
    $(shell command -v python3 2>/dev/null), \
    $(shell command -v python 2>/dev/null), \
    python3 \
)

run:
	PYTHONPATH=. $(PYTHON) src/gui/main.py

# Standard-Test
test:
	PYTHONPATH=. $(PYTHON) -m pytest

# Tests mit verbose output
test-v:
	PYTHONPATH=. $(PYTHON) -m pytest -v

# Tests mit detailliertem output und fehlgeschlagenen zuerst
test-vv:
	PYTHONPATH=. $(PYTHON) -m pytest -vv --tb=short

# Tests mit Coverage-Report
test-cov:
	PYTHONPATH=. $(PYTHON) -m pytest --cov=src.core --cov-report=term-missing

# Tests mit HTML Coverage-Report
test-cov-html:
	PYTHONPATH=. $(PYTHON) -m pytest --cov=src.core --cov-report=html
	@echo "Coverage-Report: htmlcov/index.html"

install:
	pip3 install pytest

# 4) Aufräumen: pyc-Dateien & __pycache__ löschen
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete

freeze:
	$(PYTHON) -m pip freeze > requirements.txt