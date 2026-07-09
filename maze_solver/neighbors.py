from maze_solver.constants import DIRECTIONS


def get_open_neighbors(
    maze: list[list[int]],
    position: tuple[int, int],
) -> list[tuple[tuple[int, int], str]]:
    """Return all reachable neighboring cells."""
    x, y = position
    height = len(maze)
    width = len(maze[0])
    cell = maze[y][x]

    neighbors: list[tuple[tuple[int, int], str]] = []

    for direction, (dx, dy, wall_bit) in DIRECTIONS.items():
        next_x = x + dx
        next_y = y + dy

        if next_x < 0 or next_x >= width:
            continue

        if next_y < 0 or next_y >= height:
            continue

        if cell & wall_bit:
            continue

        neighbors.append(((next_x, next_y), direction))

    return neighbors
