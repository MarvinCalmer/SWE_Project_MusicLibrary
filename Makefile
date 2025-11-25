PYTHON := $(or \
    $(shell command -v python3 2>/dev/null), \
    $(shell command -v python 2>/dev/null), \
    python3 \
)

run:
	PYTHONPATH=. $(PYTHON) src/gui/gui.py

test:
	PYTHONPATH=. $(PYTHON) -m pytest

install:
	pip install pytest

# 4) Aufräumen: pyc-Dateien & __pycache__ löschen
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete

freeze:
	$(PYTHON) -m pip freeze > requirements.txt