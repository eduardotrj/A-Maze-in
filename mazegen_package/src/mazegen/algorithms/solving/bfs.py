# Breadth-first search algorithm
# https://en.wikipedia.org/wiki/Breadth-first_search

from ...model import Maze


def solve_bfs(maze: Maze) -> str | None:
    """Find the shortest path from entry to exit using BFS."""
    queue: list[tuple[tuple[int, int], str]] = []
    visited: set[tuple[int, int]] = set()

    queue.append((maze.entry, ""))
    visited.add(maze.entry)

    while queue:
        current, path = queue.pop(0)

        if current == maze.exit:
            return path

        for neighbor, direction in maze.get_open_neighbors(current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append((neighbor, path + direction))

    return None
