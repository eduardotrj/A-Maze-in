from typing import Any
from mazegen import Maze


class PrintTerminal():
    # Intendation:
    INT_1 = '\t'
    INT_2 = '\t' * 2
    INT_3 = '\t' * 3

    # Colors:
    BHWHT: str = "\033[1;97m"
    RS: str = "\033[0m"

    @classmethod
    def clean_terminal(cls) -> None:
        print(chr(27) + "[2J")

    @classmethod
    def print_separator(cls) -> None:
        print("--------------------------------------")

    @classmethod
    def print_controls(cls) -> None:
        print(f"{cls.INT_1}{cls.BHWHT}CONTROLS:{cls.RS}")
        cls.print_separator()
        print("""
    Q -> Des/Activate Animation     W -> Show solution
    E -> Change solver              A -> Change generator
    R -> Remake                     T -> Print Maze Info
    S -> Style Before               D -> Next style
    F -> Random Exit                G -> Active/Disable Perfect
    Esc -> exit
""")

    @classmethod
    def print_maze_data(cls, maze: Maze, theme: Any, solver: Any,
                        pattern: str | None) -> None:
        """ Print basic Maze Data """
        print(f"{cls.INT_1}{cls.BHWHT}MAZE INFORMATION:{cls.RS}")
        cls.print_separator()

        algorithm = (
            "Recursive Backtracker"
            if maze.algorithm == "recursive_backtracker"
            else maze.algorithm)

        print(f"\n Size:{cls.INT_2}{maze.height}x{maze.width}"
              f"{cls.INT_2}Seed:{cls.INT_2}{maze.seed}")

        print(f" Start:{cls.INT_2}{maze.entry[0]}x{maze.entry[1]}"
              f"{cls.INT_2}Algorithm:{cls.INT_1}{algorithm}")

        print(f" Exit:{cls.INT_2}{maze.exit[0]}x{maze.exit[1]}"
              f"{cls.INT_2}Theme:{cls.INT_2}{theme}")

        print(f" Perfect:{cls.INT_1}{maze.perfect}"
              f"{cls.INT_2}Pattern:{cls.INT_1}{pattern}")

        print(f" Solver:{cls.INT_1}{solver}")

    @classmethod
    def print_title(cls, logo: str) -> None:  # noqa: E731
        print(logo)
