UV			:= uv
PYTHON_VERSION := 3.11
PYTHON      := python3.11
POETRY      := poetry
MAIN        := a_maze_ing.py
VENV        := .venv
CONFIG		:= config.txt

PACKAGE_DIR 		:= mazegen_package
PACKAGE_DIST 		:= $(PACKAGE_DIR)/dist
PACKAGE_BUILD_VENV 	:= .venv-package-build

.PHONY: install run debug clean clean-all lint lint-strict \
	package package-clean

# if no 3.11.14 version find we have to install this version:
# uv python install 3.11.14

install:
	$(POETRY) config virtualenvs.in-project true --local
	$(POETRY) env use $(PYTHON)
	# if uv is used to install python3.11
	# (POETRY) env use $(uv python find 3.11)
	$(POETRY) install
	$(POETRY) run python -m pip install -e $(PACKAGE_DIR)

run: install
	$(POETRY) run python $(MAIN) $(CONFIG)

debug: install
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
	rm -f poetry.toml

lint:
	$(POETRY) run flake8 . --exclude=.venv,__pycache__,.mypy_cache,.pytest_cache,.ruff_cache,build,dist
	$(POETRY) run mypy . \
		--exclude '(^|/)(\.venv|__pycache__|\.mypy_cache|\.pytest_cache|\.ruff_cache|build|dist)/' \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(POETRY) run flake8 . --exclude=.venv,__pycache__,.mypy_cache,.pytest_cache,.ruff_cache,build,dist
	$(POETRY) run mypy . \
		--exclude '(^|/)(\.venv|__pycache__|\.mypy_cache|\.pytest_cache|\.ruff_cache|build|dist)/' \
		--strict

package:
	rm -rf $(PACKAGE_BUILD_VENV)
	rm -rf $(PACKAGE_DIST)
	rm -rf $(PACKAGE_DIR)/build
	rm -rf $(PACKAGE_DIR)/src/*.egg-info

	$(UV) venv \
		--python $(PYTHON_VERSION) \
		$(PACKAGE_BUILD_VENV)

	$(UV) pip install \
		--python $(PACKAGE_BUILD_VENV)/bin/python \
		build

	$(PACKAGE_BUILD_VENV)/bin/python -m build \
		--outdir $(PACKAGE_DIST) \
		$(PACKAGE_DIR)

	rm -f mazegen-*.whl mazegen-*.tar.gz
	cp $(PACKAGE_DIST)/mazegen-*.whl .
	cp $(PACKAGE_DIST)/mazegen-*.tar.gz .

	@echo "Package created:"
	@ls -1 mazegen-*.whl mazegen-*.tar.gz

package-clean:
	rm -rf $(PACKAGE_BUILD_VENV)
	rm -rf $(PACKAGE_DIST)
	rm -rf $(PACKAGE_DIR)/build
	rm -rf $(PACKAGE_DIR)/src/*.egg-info