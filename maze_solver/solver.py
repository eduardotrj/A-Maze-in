from maze_solver.algorithms.bfs import solve_bfs
from maze_solver.algorithms.dfs import solve_dfs
from maze_solver.algorithms.dijkstra import solve_dijkstra
from maze_solver.algorithms.astar import solve_astar


def solve_maze(
    maze: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int],
    algorithm: str = "bfs",
) -> str | None:
    """Solve a maze with the selected algorithm."""
    if algorithm == "bfs":
        return solve_bfs(maze, start, end)

    if algorithm == "dfs":
        return solve_dfs(maze, start, end)

    if algorithm == "dijkstra":
        return solve_dijkstra(maze, start, end)

    if algorithm == "astar":
        return solve_astar(maze, start, end)

    raise ValueError(f"Unknown solving algorithm: {algorithm}")
