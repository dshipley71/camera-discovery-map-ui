test:
	PYTHONPATH=src python -m pytest -q

lint:
	python -m ruff check src tests

typecheck:
	python -m mypy src/camera_discovery_map_ui

compile:
	python -m compileall -q src tests

check: compile test lint typecheck
