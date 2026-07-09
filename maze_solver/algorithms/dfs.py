# Depth-first search algorithm
# https://en.wikipedia.org/wiki/Depth-first_search

from maze_solver.neighbors import get_open_neighbors


def solve_dfs(
    maze: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> str | None:
    """Find any valid path using depth-first search."""
    visited: set[tuple[int, int]] = set()

    def dfs(position: tuple[int, int], path: str) -> str | None:
        if position == end:
            return path

        visited.add(position)

        for next_position, direction in get_open_neighbors(maze, position):
            if next_position in visited:
                continue

            result = dfs(next_position, path + direction)

            if result is not None:
                return result

        return None

    return dfs(start, "")
