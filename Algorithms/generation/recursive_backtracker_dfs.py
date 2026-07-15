import random

from Maze.grid import (
    Position,
    create_full_walled_grid,
    freeze_grid,
    get_unvisited_neighbors,
    remove_wall,
)


def generate_recursive_backtracker_dfs(
    width: int,
    height: int,
    seed: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Generate a perfect maze using randomized iterative DFS backtracking."""
    random_generator = random.Random(seed)
    grid = create_full_walled_grid(width, height)

    start: Position = (0, 0)
    visited: set[Position] = {start}
    stack: list[Position] = [start]

    while stack:
        current = stack[-1]
        neighbors = get_unvisited_neighbors(
            position=current,
            width=width,
            height=height,
            visited=visited,
        )

        if not neighbors:
            stack.pop()
            continue

        next_position, wall = random_generator.choice(neighbors)

        remove_wall(
            grid=grid,
            current=current,
            neighbor=next_position,
            wall=wall,
        )

        visited.add(next_position)
        stack.append(next_position)

    return freeze_grid(grid)
