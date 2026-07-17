from Maze.model import Maze
from Maze.solver import MazeSolver

# to test:
# go to root folder and run:
# poetry run python -m Tests.maze_solver_test

raw_maze = [
    "939551553",
    "AC693A93E",
    "E93AE86C3",
    "96869457A",
    "AFAFAFFFA",
    "AFEF857FA",
    "AFFFAFFFA",
    "A93FAFD52",
    "C6AFEFFFA",
    "B9693D152",
    "8696C56BA",
    "A96917946",
    "C6D6C5457",
]

raw_solutuon = "NWSSWNWSWSSSSSENESSWSWSSENENENESEENEENNNNNNNWNWS"


def convert_rows(lines: list[str]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(int(char, 16) for char in line)
        for line in lines
    )


def main() -> None:
    maze = Maze(
        rows=convert_rows(raw_maze),
        entry=(4, 2),
        exit=(6, 2),
        record=[],
        algorithm="test",
        seed=0,
    )

    for algorithm in MazeSolver.list_solvers():
        solution = MazeSolver.solve(
            maze,
            algorithm,
        )

        print(f"{algorithm}: {solution}")


if __name__ == "__main__":
    main()
