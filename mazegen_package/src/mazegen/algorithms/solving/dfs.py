# Depth-first search algorithm
# https://en.wikipedia.org/wiki/Depth-first_search

from mazegen.model import Maze


def solve_dfs(maze: Maze) -> str | None:
    """Find any valid path using depth-first search."""
    visited: set[tuple[int, int]] = set()

    def dfs(position: tuple[int, int], path: str) -> str | None:
        if position == maze.exit:
            return path

        visited.add(position)

        for next_position, direction in maze.get_open_neighbors(position):
            if next_position in visited:
                continue

            result = dfs(next_position, path + direction)

            if result is not None:
                return result

        return None

    return dfs(maze.entry, "")
