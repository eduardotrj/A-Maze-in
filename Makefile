UV              := uv
PYTHON_VERSION  := 3.11
PYTHON          := python3.11
POETRY          := poetry
MAIN            := a_maze_ing.py
VENV            := .venv
CONFIG          := config.txt

PACKAGE_DIR        := mazegen_package
PACKAGE_DIST       := $(PACKAGE_DIR)/dist
PACKAGE_BUILD_VENV := .venv-package-build
PACKAGE_TEST_VENV  := .venv-package-test

.PHONY: install run debug clean clean-all lint lint-strict \
	package package-test package-clean

install:
	$(POETRY) config virtualenvs.in-project true --local
	$(POETRY) env use $(PYTHON)
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
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean package-clean
	rm -rf $(VENV)
	rm -f poetry.toml

lint:
	$(POETRY) run flake8 . \
		--exclude=.venv,.venv-package-build,.venv-package-test,logo.py,Test,Tests,mlx,__pycache__,.mypy_cache,.pytest_cache,.ruff_cache,build,dist

	MYPYPATH=$(PACKAGE_DIR)/src $(POETRY) run mypy \
		$(MAIN) Config Graphics \
		--exclude '(^|/)(\.venv|\.venv-package-build|\.venv-package-test|__pycache__|Test|Tests|\.mypy_cache|\.pytest_cache|\.ruff_cache|build|dist|mazegen_package)/' \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

	MYPYPATH=$(PACKAGE_DIR)/src $(POETRY) run mypy \
		-p mazegen \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(POETRY) run flake8 . \
		--exclude=.venv,.venv-package-build,.venv-package-test,logo.py,Test,Tests,mlx,__pycache__,.mypy_cache,.pytest_cache,.ruff_cache,build,dist

	MYPYPATH=$(PACKAGE_DIR)/src $(POETRY) run mypy \
		$(MAIN) Config Graphics \
		--exclude '(^|/)(\.venv|\.venv-package-build|\.venv-package-test|__pycache__|Test|Tests|\.mypy_cache|\.pytest_cache|\.ruff_cache|build|dist|mazegen_package)/' \
		--strict

	MYPYPATH=$(PACKAGE_DIR)/src $(POETRY) run mypy \
		-p mazegen \
		--strict

package:
	rm -rf $(PACKAGE_BUILD_VENV)
	rm -rf $(PACKAGE_DIST)
	rm -rf $(PACKAGE_DIR)/build
	rm -rf $(PACKAGE_DIR)/src/*.egg-info
	rm -f mazegen-*.whl mazegen-*.tar.gz

	$(UV) venv --python $(PYTHON_VERSION) $(PACKAGE_BUILD_VENV)

	$(UV) pip install \
		--python $(PACKAGE_BUILD_VENV)/bin/python \
		build

	$(PACKAGE_BUILD_VENV)/bin/python -m build \
		--outdir $(PACKAGE_DIST) \
		$(PACKAGE_DIR)

	cp $(PACKAGE_DIST)/mazegen-*.whl .
	cp $(PACKAGE_DIST)/mazegen-*.tar.gz .

	@echo "Package created:"
	@ls -1 mazegen-*.whl mazegen-*.tar.gz

package-test: package
	rm -rf $(PACKAGE_TEST_VENV)

	$(UV) venv --python $(PYTHON_VERSION) $(PACKAGE_TEST_VENV)

	$(UV) pip install \
		--python $(PACKAGE_TEST_VENV)/bin/python \
		./mazegen-*.whl

	$(PACKAGE_TEST_VENV)/bin/python -c "from mazegen import Generator, MazeSolver, PATTERN; maze = Generator.generate_maze(width=41, height=31, entry=(0, 0), exit=(19, 14), name='prim', pattern=PATTERN['P_42'], seed=42, perfect=True); solution = MazeSolver.solve(maze, 'bfs'); print('Maze rows:', len(maze.rows)); print('Seed:', maze.seed); print('Solution found:', solution is not None)"

package-clean:
	rm -rf $(PACKAGE_BUILD_VENV)
	rm -rf $(PACKAGE_TEST_VENV)
	rm -rf $(PACKAGE_DIST)
	rm -rf $(PACKAGE_DIR)/build
	rm -rf $(PACKAGE_DIR)/src/*.egg-info
