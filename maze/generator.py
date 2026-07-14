from algorithms.generation import generate_recursive_backtracker_dfs
from maze.model import Maze


def generate_maze(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    seed: int | None = None,
    perfect: bool = True,
    algorithm: str = "recursive_backtracker_dfs",
) -> Maze:
    """Generate and return a Maze object with the selected algorithm."""
    if algorithm == "recursive_backtracker_dfs":
        rows = generate_recursive_backtracker_dfs(
            width=width,
            height=height,
            seed=seed,
        )
    else:
        raise ValueError(f"Unknown generation algorithm: {algorithm}")

    return Maze(
        rows=rows,
        entry=entry,
        exit=exit_,
        seed=seed,
        perfect=perfect,
    )
