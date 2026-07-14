from utils.constants import ALL_WALLS, DIRECTIONS, OPPOSITE_WALL


Position = tuple[int, int]
Grid = list[list[int]]


def create_full_walled_grid(width: int, height: int) -> Grid:
    """Create a grid in which every cell initially has all four walls."""
    return [
        [ALL_WALLS for _ in range(width)]
        for _ in range(height)
    ]


def get_unvisited_neighbors(
    position: Position,
    width: int,
    height: int,
    visited: set[Position],
) -> list[tuple[Position, int]]:
    """Return unvisited neighboring cells and the wall toward each one."""
    x, y = position
    neighbors: list[tuple[Position, int]] = []

    for dx, dy, wall in DIRECTIONS.values():
        next_x = x + dx
        next_y = y + dy
        next_position = (next_x, next_y)

        if next_x < 0 or next_x >= width:
            continue

        if next_y < 0 or next_y >= height:
            continue

        if next_position in visited:
            continue

        neighbors.append((next_position, wall))

    return neighbors


def remove_wall(
    grid: Grid,
    current: Position,
    neighbor: Position,
    wall: int,
) -> None:
    """Remove the shared wall between two neighboring cells."""
    current_x, current_y = current
    neighbor_x, neighbor_y = neighbor

    grid[current_y][current_x] &= ~wall
    grid[neighbor_y][neighbor_x] &= ~OPPOSITE_WALL[wall]


def freeze_grid(grid: Grid) -> tuple[tuple[int, ...], ...]:
    """Convert a mutable generation grid into immutable maze rows."""
    return tuple(tuple(row) for row in grid)
