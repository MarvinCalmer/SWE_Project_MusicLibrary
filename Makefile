run:
	PYTHONPATH=. python3 src/gui/gui.py
test:
	PYTHONPATH=. pytest

install:
	pip install pytest

# 4) Aufräumen: pyc-Dateien & __pycache__ löschen
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
