from algorithms import solve_bfs, solve_dfs
from maze.model import Maze

# to test:
# go to root folder and run:
# poetry run python -m tests.maze_solver_test

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
        seed=0,
    )

    solution = solve_bfs(maze)

    print(solution)
    if raw_solutuon == solution:
        print("BFS algorithm works!!")
    else:
        print("Please try again :(")
 
    solution = solve_dfs(maze)

    print(solution)
    if raw_solutuon == solution:
        print("DFS algorithm works!!")
    else:
        print("Please try again :(")


if __name__ == "__main__":
    main()
