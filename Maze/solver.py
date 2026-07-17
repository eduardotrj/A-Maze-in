"""Provide a common interface for maze solving algorithms."""

from Algorithms.solving.astar import solve_astar
from Algorithms.solving.bfs import solve_bfs
from Algorithms.solving.dfs import solve_dfs
from Algorithms.solving.dijkstra import solve_dijkstra
from Maze.model import Maze


class MazeSolver:
    """Select and execute maze solving algorithms."""

    @staticmethod
    def list_solvers() -> list[str]:
        """Return available solver names."""
        return [
            "bfs",
            "dfs",
            "astar",
            "dijkstra",
        ]

    @staticmethod
    def solve(
        maze: Maze,
        name: str = "bfs",
    ) -> str | None:
        """Solve the maze using the selected algorithm."""
        solver_name = name.lower()

        if solver_name == "bfs":
            return solve_bfs(maze)

        if solver_name == "dfs":
            return solve_dfs(maze)

        if solver_name == "astar":
            return solve_astar(maze)

        if solver_name == "dijkstra":
            return solve_dijkstra(maze)

        available = ", ".join(
            MazeSolver.list_solvers()
        )

        raise ValueError(
            f"Unknown solver: {name}. "
            f"Available solvers: {available}"
        )