# mazegen

Reusable maze-generation and solving package created for the 42 A-Maze-ing project.

## Features

- Randomized Prim
- Kruskal
- Recursive Backtracker
- Seeded reproducible generation
- Fully closed `42` pattern cells
- BFS, DFS, Dijkstra, and A* solving
- Access to the generated wall structure and solution

## Install a built wheel

From the A-Maze-ing repository root:

```bash
python -m pip install ./mazegen-1.0.0-py3-none-any.whl
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
)

solution = MazeSolver.solve(maze, "bfs")

print(maze.rows)
print(solution)
```

## Custom parameters

```python
maze = Generator.generate_maze(
    width=31,
    height=21,
    entry=(0, 0),
    exit=(14, 9),
    name="kruskal",
    pattern=None,
    seed=1234,
)
```

The generator currently receives internal wall-grid dimensions. For a logical maze of `W x H` cells, pass:

```python
width = W * 2 + 1
height = H * 2 + 1
```

Entry and exit remain logical zero-based cell coordinates.

Available generator names:

```text
prim
kruskal
recursive_backtracker
```

## Access the generated structure

```python
print(maze.rows)
print(maze.width, maze.height)
print(maze.entry, maze.exit)
print(maze.seed)
print(maze.algorithm)
print(maze.pattern_cells)
```

Each value in `maze.rows` is a four-bit wall mask:

| Bit | Direction |
|---:|---|
| `0` | North |
| `1` | East |
| `2` | South |
| `3` | West |

A set bit means that the wall is closed.

## Solve a maze

```python
shortest_path = MazeSolver.solve(maze, "bfs")
astar_path = MazeSolver.solve(maze, "astar")
dijkstra_path = MazeSolver.solve(maze, "dijkstra")
any_valid_path = MazeSolver.solve(maze, "dfs")
```

The result is a string containing only:

```text
N E S W
```

BFS, Dijkstra, and A* are intended for shortest-path use. DFS returns a valid path but does not guarantee the shortest path.

## Build the package

From the repository root:

```bash
make package
```

The command creates:

```text
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
```