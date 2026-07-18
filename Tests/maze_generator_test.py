"""Test maze generation and seed reproducibility."""

from Maze.generator import Generator
from Maze.solver import MazeSolver


# To test from the project root:
# poetry run python -m Tests.maze_generator_test


def rows_as_hex(rows: tuple[tuple[int, ...], ...]) -> str:
    """Return maze rows in hexadecimal form for visual inspection."""
    return "\n".join(
        "".join(format(cell, "X") for cell in row)
        for row in rows
    )


def main() -> None:
    """Generate the same seeded maze twice and solve it with BFS."""
    logical_width = 10
    logical_height = 8

    first = Generator.generate_maze(
        width=logical_width * 2 + 1,
        height=logical_height * 2 + 1,
        entry=(0, 0),
        exit=(9, 7),
        name="prim",
        pattern=None,
        seed=42,
    )

    second = Generator.generate_maze(
        width=logical_width * 2 + 1,
        height=logical_height * 2 + 1,
        entry=(0, 0),
        exit=(9, 7),
        name="prim",
        pattern=None,
        seed=42,
    )

    print(rows_as_hex(first.rows))
    print()

    if first.rows == second.rows:
        print("Seed reproducibility works!")
    else:
        print("Seed reproducibility failed.")

    solution = MazeSolver.solve(
        first,
        name="bfs",
    )

    print(f"Shortest path: {solution}")


if __name__ == "__main__":
    main()
