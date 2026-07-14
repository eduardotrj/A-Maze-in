# Dijkstra's algorithm
# https://en.wikipedia.org/wiki/Dijkstra's_algorithm


from maze.model import Maze


def solve_dijkstra(maze: Maze) -> str | None:
    """Find the shortest path using Dijkstra's algorithm."""
    queue: list[tuple[int, tuple[int, int], str]] = [
        (0, maze.entry, "")
    ]

    best_cost: dict[tuple[int, int], int] = {
        maze.entry: 0,
    }

    while queue:
        queue.sort(key=lambda item: item[0])

        current_cost, current, path = queue.pop(0)

        if current == maze.exit:
            return path

        for next_position, direction in maze.get_open_neighbors(current):
            new_cost = current_cost + 1

            if (
                next_position in best_cost
                and new_cost >= best_cost[next_position]
            ):
                continue

            best_cost[next_position] = new_cost

            queue.append(
                (
                    new_cost,
                    next_position,
                    path + direction,
                )
            )

    return None
