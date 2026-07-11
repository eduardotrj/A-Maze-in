# Breadth-first search algorithm
# https://en.wikipedia.org/wiki/Breadth-first_search

from maze_solver.neighbors import get_open_neighbors


def solve_bfs(
    maze: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> str | None:
    """Find the shortest path from start to end using BFS."""
    queue: list[tuple[tuple[int, int], str]] = []
    visited: set[tuple[int, int]] = set()

    queue.append((start, ""))
    visited.add(start)

    while queue:
        current, path = queue.pop(0)

        if current == end:
            return path

        for neighbor, direction in get_open_neighbors(maze, current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append((neighbor, path + direction))

    return None
