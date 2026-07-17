from Maze.generator import generate_maze
from Maze.solver import solve_maze


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
    first = generate_maze(
        width=10,
        height=8,
        entry=(0, 0),
        exit_=(9, 7),
        seed=42,
    )
    second = generate_maze(
        width=10,
        height=8,
        entry=(0, 0),
        exit_=(9, 7),
        seed=42,
    )

    print(rows_as_hex(first.rows))
    print()

    if first.rows == second.rows:
        print("Seed reproducibility works!!")
    else:
        print("Seed reproducibility failed :(")

    solution = solve_maze(first, algorithm="bfs")
    print(f"Shortest path: {solution}")


if __name__ == "__main__":
    main()
