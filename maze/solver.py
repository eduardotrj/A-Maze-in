from algorithms import solve_dfs, solve_bfs, solve_astar, solve_dijkstra
from maze.model import Maze


def solve_maze(
    maze: Maze,
    algorithm: str = "bfs",
) -> str | None:
    """Solve the maze using the selected algorithm."""
    if algorithm == "bfs":
        return solve_bfs(maze)

    if algorithm == "dfs":
        return solve_dfs(maze)

    if algorithm == "dijkstra":
        return solve_dijkstra(maze)

    if algorithm == "astar":
        return solve_astar(maze)

    raise ValueError(f"Unknown solving algorithm: {algorithm}")
