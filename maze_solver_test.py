from maze_solver import parse_maze, solve_dfs


raw_maze = ["939551553",
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
            "C6D6C5457"
            ]

raw_start = (4, 2)
raw_end = (6, 2)
raw_solutuon = "NWSSWNWSWSSSSSENESSWSWSSENENENESEENEENNNNNNNWNWS"


def main() -> None:

    maze = parse_maze(raw_maze)
    print(maze)
    solution = solve_dfs(maze, raw_start, raw_end)
    print(solution)
    if raw_solutuon == solution:
        print("It works!!")
    else:
        print("Please try again :(")


if __name__ == "__main__":
    main()
