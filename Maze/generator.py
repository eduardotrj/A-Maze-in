"""Provide a common interface for maze generation algorithms."""

from typing import Any, Literal, TypeAlias

from Algorithms.generation.kruskal import Kruskal
from Algorithms.generation.maze_generator import MazeGenerator
from Algorithms.generation.prim import Prim
from Algorithms.generation.recursive_backtracker import Backtracker
from Algorithms.generation.hunt_and_kill import HuntAndKill
from Algorithms.generation.eller import Eller
from Maze.model import Maze

# def generate_maze(
#    width: int,
#    height: int,
#    entry: tuple[int, int],
#    exit_: tuple[int, int],
#    seed: int | None = None,
#    perfect: bool = True,
#    algorithm: str = "recursive_backtracker_dfs",
# ) -> Maze:
#    """Generate and return a Maze object with the selected algorithm."""
#    if algorithm == "recursive_backtracker_dfs":
#        rows = generate_recursive_backtracker_dfs(
#            width=width,
#            height=height,
#            seed=seed,
#        )
#    else:
#        raise ValueError(f"Unknown generation algorithm: {algorithm}")

#    return Maze(
#        rows=rows,
#        entry=entry,
#        exit=exit_,
#        seed=seed,
#        perfect=perfect,
#    )

GeneratorName: TypeAlias = Literal[
    "recursive_backtracker",
    "kruskal",
    "prim",
    "huntandkill",
    "eller"
]

Pattern: TypeAlias = tuple[tuple[Any, ...], ...]


class Generator:
    """Select and run maze generation algorithms."""

    _generators: dict[
        GeneratorName,
        type[MazeGenerator],
    ] = {
        "recursive_backtracker": Backtracker,
        "kruskal": Kruskal,
        "prim": Prim,
        "huntandkill": HuntAndKill,
        "eller": Eller
    }

    @classmethod
    def list_generators(cls) -> list[GeneratorName]:
        """Return the available generator names."""
        return list(cls._generators)

    @classmethod
    def normalize_name(cls, name: str) -> GeneratorName:
        """Validate and normalize a generator name."""
        normalized_name = name.strip().lower()

        if normalized_name == "recursive_backtracker":
            return "recursive_backtracker"

        if normalized_name == "kruskal":
            return "kruskal"

        if normalized_name == "prim":
            return "prim"

        if normalized_name == "huntandkill":
            return "huntandkill"
        
        if normalized_name == "eller":
            return "eller"

        available = ", ".join(cls.list_generators())

        raise ValueError(
            f"Unknown generator: {name}. "
            f"Available generators: {available}"
        )

    @classmethod
    def create(
        cls,
        name: str,
        width: int,
        height: int,
        seed: int | None = None,
    ) -> MazeGenerator:
        """Create the selected maze generator."""
        generator_name = cls.normalize_name(name)
        generator_class = cls._generators[generator_name]

        return generator_class(
            width,
            height,
            seed,
        )

    @staticmethod
    def binary_to_hexa(
        maze: list[list[int]],
    ) -> list[list[int]]:
        """Convert the internal map to four-bit wall masks."""
        north = 1
        east = 2
        south = 4
        west = 8

        height = len(maze)
        width = len(maze[0])

        output: list[list[int]] = []

        for row in range(1, height, 2):
            output_row: list[int] = []

            for column in range(1, width, 2):
                mask = 0

                if maze[row - 1][column] == 1:
                    mask |= north

                if maze[row][column + 1] == 1:
                    mask |= east

                if maze[row + 1][column] == 1:
                    mask |= south

                if maze[row][column - 1] == 1:
                    mask |= west

                output_row.append(mask)

            output.append(output_row)

        return output

    @classmethod
    def generate_maze(
        cls,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        name: str = "prim",
        pattern: Pattern | None = None,
        seed: int | None = None,
        perfect: bool = True,
    ) -> Maze:
        """Generate and return a Maze object."""
        generator_name = cls.normalize_name(name)

        internal_entry = (
            entry[0] * 2 + 1,
            entry[1] * 2 + 1,
        )

        internal_exit = (
            exit[0] * 2 + 1,
            exit[1] * 2 + 1,
        )

        generator = cls.create(
            name=generator_name,
            width=width,
            height=height,
            seed=seed,
        )

        generator.generate(
            width=width,
            height=height,
            entry=internal_entry,
            exit=internal_exit,
            pattern=pattern,
            seed=seed,
            perfect=perfect,
        )

        output = cls.binary_to_hexa(
            generator.get_maze()
        )

        final_rows = tuple(
            tuple(row)
            for row in output
        )

        return Maze(
            rows=final_rows,
            entry=entry,
            exit=exit,
            record=generator.get_record(),
            algorithm=generator_name,
            seed=generator.get_seed(),
            perfect=generator.is_perfect(),
            pattern=generator.get_pattern(),
            pattern_cells=generator.get_pattern_cells(),
        )
