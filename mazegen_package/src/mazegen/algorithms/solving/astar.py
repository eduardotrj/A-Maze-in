# A* search algorithm
# https://en.wikipedia.org/wiki/A*_search_algorithm


from mazegen.model import Maze


def solve_astar(maze: Maze) -> str | None:
    """Find the shortest path using the A* search algorithm."""

    def heuristic(position: tuple[int, int]) -> int:
        """Calculate Manhattan distance to the exit."""
        x1, y1 = position
        x2, y2 = maze.exit

        return abs(x1 - x2) + abs(y1 - y2)

    queue: list[
        tuple[int, int, tuple[int, int], str]
    ] = [
        (
            heuristic(maze.entry),
            0,
            maze.entry,
            "",
        )
    ]

    best_cost: dict[tuple[int, int], int] = {
        maze.entry: 0,
    }

    while queue:
        queue.sort(key=lambda item: item[0])

        _, current_cost, current, path = queue.pop(0)

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

            estimated_total_cost = (
                new_cost + heuristic(next_position)
            )

            queue.append(
                (
                    estimated_total_cost,
                    new_cost,
                    next_position,
                    path + direction,
                )
            )

    return None
