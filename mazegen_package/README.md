# mazegen

Reusable maze generation and solving package created for the 42 A-Maze-ing project.

`mazegen` contains the core maze logic of the project: maze model, generation algorithms, solving algorithms, utility functions, wall representation, pattern handling, and package-level API.

The graphical application `a_maze_ing.py` uses this package to generate and solve mazes.

## Features

- Randomized Prim maze generation
- Kruskal maze generation
- Recursive Backtracker maze generation
- Hunt-and-Kill maze generation
- Seeded reproducible generation
- Optional non-perfect maze generation
- Optional locked `42` pattern cells
- BFS, DFS, Dijkstra, and A* solving
- Access to the generated wall structure, seed, metadata, and solution path
- Buildable as both `.whl` and `.tar.gz`

## Build the package

From the A-Maze-ing repository root:

```bash
make package
```

This command creates the package files in the repository root:

```text
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
```

It also creates the same files under:

```text
mazegen_package/dist/
```

To remove generated package files:

```bash
make package-clean
```

## Test the built package

From the repository root:

```bash
make package-test
```

This creates a separate virtual environment, installs the newly built wheel, imports `mazegen`, generates a maze, solves it, and prints basic information.

This is useful for checking that the package works outside the main project environment.

## Install a built wheel manually

From the A-Maze-ing repository root:

```bash
python -m pip install ./mazegen-1.0.0-py3-none-any.whl
```

After installation, the package can be imported with:

```python
import mazegen
```

## Basic use

```python
from mazegen import Generator, MazeSolver, PATTERN

logical_width = 20
logical_height = 15

maze = Generator.generate_maze(
    width=logical_width * 2 + 1,
    height=logical_height * 2 + 1,
    entry=(0, 0),
    exit=(19, 14),
    name="prim",
    pattern=PATTERN["P_42"],
    seed=42,
    perfect=True,
)

solution = MazeSolver.solve(maze, "bfs")

print(maze.rows)
print(solution)
```

## Custom parameters

```python
from mazegen import Generator, MazeSolver

maze = Generator.generate_maze(
    width=31,
    height=21,
    entry=(0, 0),
    exit=(14, 9),
    name="kruskal",
    pattern=None,
    seed=1234,
    perfect=True,
)

solution = MazeSolver.solve(maze, "bfs")

print(maze.seed)
print(solution)
```

## Dimensions

The generator receives internal wall-grid dimensions.

For a logical maze of `W x H` cells, pass:

```python
width = W * 2 + 1
height = H * 2 + 1
```

For example, a logical maze of `20 x 15` cells should be generated with:

```python
width = 41
height = 31
```

Entry and exit remain logical zero-based cell coordinates:

```python
entry = (0, 0)
exit = (19, 14)
```

## Available generation algorithms

```text
prim
kruskal
recursive_backtracker
hunt_and_kill
```

The selected algorithm is passed with the `name` parameter:

```python
maze = Generator.generate_maze(
    width=41,
    height=31,
    entry=(0, 0),
    exit=(19, 14),
    name="hunt_and_kill",
    pattern=None,
    seed=42,
    perfect=True,
)
```

## Perfect and non-perfect mazes

If `perfect=True`, the generator should create a perfect maze whenever the selected algorithm supports it.

A perfect maze has exactly one valid path between any two reachable cells.

```python
maze = Generator.generate_maze(
    width=41,
    height=31,
    entry=(0, 0),
    exit=(19, 14),
    name="prim",
    pattern=None,
    seed=42,
    perfect=True,
)
```

If `perfect=False`, the generator may open additional walls to create loops:

```python
maze = Generator.generate_maze(
    width=41,
    height=31,
    entry=(0, 0),
    exit=(19, 14),
    name="prim",
    pattern=None,
    seed=42,
    perfect=False,
)
```

## Seed behavior

If a seed is provided, the same algorithm with the same parameters should generate the same maze:

```python
maze = Generator.generate_maze(
    width=41,
    height=31,
    entry=(0, 0),
    exit=(19, 14),
    name="prim",
    pattern=None,
    seed=42,
    perfect=True,
)
```

If `seed=None`, the package generates a random seed internally. The generated seed can be accessed from the maze object:

```python
print(maze.seed)
```

This makes the maze reproducible later by reusing that seed.

## Access the generated structure

```python
print(maze.rows)
print(maze.width, maze.height)
print(maze.entry, maze.exit)
print(maze.seed)
print(maze.algorithm)
print(maze.pattern_cells)
```

Each value in `maze.rows` is a four-bit wall mask.

| Bit | Direction |
|---:|---|
| `0` | North |
| `1` | East |
| `2` | South |
| `3` | West |

A set bit means that the wall is closed.

For example:

```text
15
```

means all four walls are closed.

```text
0
```

means all four walls are open.

## Solve a maze

```python
shortest_path = MazeSolver.solve(maze, "bfs")
astar_path = MazeSolver.solve(maze, "astar")
dijkstra_path = MazeSolver.solve(maze, "dijkstra")
any_valid_path = MazeSolver.solve(maze, "dfs")
```

The result is a string containing only these directions:

```text
N E S W
```

BFS, Dijkstra, and A* are intended for shortest-path use.

DFS returns a valid path but does not guarantee the shortest path.

## Available solving algorithms

```text
bfs
dfs
dijkstra
astar
```

Recommended default solver:

```text
bfs
```

## Example: generate and solve

```python
from mazegen import Generator, MazeSolver, PATTERN

maze = Generator.generate_maze(
    width=41,
    height=31,
    entry=(0, 0),
    exit=(19, 14),
    name="recursive_backtracker",
    pattern=PATTERN["P_42"],
    seed=2026,
    perfect=True,
)

solution = MazeSolver.solve(maze, "bfs")

if solution is None:
    print("No valid path found")
else:
    print("Solution:", solution)
    print("Seed:", maze.seed)
```

## Use with the main application

The main A-Maze-ing application can be run from the repository root with:

```bash
make run
```

or manually:

```bash
poetry run python a_maze_ing.py config.txt
```

The application reads the configuration file, calls `mazegen`, displays the maze, solves it, and writes the output file.

## Package structure

```text
mazegen_package/
├── README.md
├── pyproject.toml
└── src/
    └── mazegen/
        ├── __init__.py
        ├── model.py
        ├── generator.py
        ├── solver.py
        ├── grid.py
        ├── exporter.py
        ├── patterns.py
        ├── algorithms/
        │   ├── generation/
		│	│	├── __init__.py/
		│	│	├── maze_generator.py/
		│	│	├── eller.py/
		│	│	├── hunt_and_kill.py/
		│	│	├── kruskal.py/
		│	│	├── prim.py/
		│	│	└── recursive_backtracker.py/
        │   └── solving/
		│	│	├── __init__.py/
		│	│	├── bfs.py/
		│	│	├── dfs.py/
		│	│	├── djikstra.py/
		│	│	└── astar.py/
        └── utils/
		│	├── __init__.py/
		│	├── constants.py/
		│	└── neighbors.py/
```

## Notes

This package is intentionally independent from the graphical interface.

It does not require MiniLibX or the main application window to generate and solve a maze.