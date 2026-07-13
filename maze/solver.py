from algorithms.solving.astar import solve_astar
from algorithms.solving.bfs import solve_bfs
from algorithms.solving.dfs import solve_dfs
from algorithms.solving.dijkstra import solve_dijkstra

from maze.model import Maze


def solve_maze(
    maze: Maze,
    algorithm: str = "bfs",
) -> str | None:
    """Solve a maze using the selected algorithm."""
    solvers = {
        "bfs": solve_bfs,
        "dfs": solve_dfs,
        "astar": solve_astar,
        "dijkstra": solve_dijkstra,
    }

    if algorithm not in solvers:
        raise ValueError(
            f"Unknown solving algorithm: {algorithm}"
        )

    return solvers[algorithm](maze)
