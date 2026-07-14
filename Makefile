PYTHON      := python3.11
POETRY      := poetry
MAIN        := config_test.py
# MAIN        := a_maze_ing.py
VENV        := .venv
CONFIG		:= config.txt

.PHONY: install run debug clean clean-all lint lint-strict

# if no 3.11.14 version find we have to install this version:
# uv python install 3.11.14

install:
	$(POETRY) config virtualenvs.in-project true --local
	$(POETRY) env use $(PYTHON)
	# if uv is used to install python3.11
	# (POETRY) env use $(uv python find 3.11)
	$(POETRY) install

run:
	$(POETRY) run python $(MAIN) $(CONFIG)

debug:
	$(POETRY) run python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean
	rm -rf $(VENV)
	rm -f poetry.lock
	rm -f poetry.toml

lint:
	$(POETRY) run flake8 .
	$(POETRY) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(POETRY) run flake8 .
	$(POETRY) run mypy . --strict