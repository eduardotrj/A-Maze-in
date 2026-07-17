from typing import Dict, Type, Any

import Algorithms.generation.recursive_backtracker as rb
import Algorithms.generation.kruskal as kr
import Algorithms.generation.prim as pr
# from algorithms.generation import generate_recursive_backtracker_dfs
from Algorithms.generation.maze_generator import MazeGenerator
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


class Generator:
    """Select and run maze generation algorithms."""

    _generators: dict[str, type[MazeGenerator]] = {
        "recursive_backtracker": rb.Backtracker,
        "kruskal": kr.Kruskal,
        "prim": pr.Prim,
    }

    @classmethod
    def list_generators(cls) -> list[str]:
        """Return the available generator names."""
        return sorted(cls._generators)

    @classmethod
    def create(
        cls,
        name: str,
        width: int,
        height: int,
        seed: int | None = None,
    ) -> MazeGenerator:
        """Create the selected maze generator."""
        normalized_name = name.strip().lower()
        generator_class = cls._generators.get(normalized_name)

        if generator_class is None:
            available = ", ".join(cls.list_generators())
            raise ValueError(
                f"Unknown generator: {name}. "
                f"Available generators: {available}"
            )

        return generator_class(width, height, seed)

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

    @staticmethod
    def generate_maze(
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        name: str = "prim",
        pattern: tuple[tuple[Any, ...], ...] | None = None,
        seed: int | None = None,
    ) -> Maze:
        """Generate and return a Maze object."""
        internal_entry = (
            entry[0] * 2 + 1,
            entry[1] * 2 + 1,
        )
        internal_exit = (
            exit[0] * 2 + 1,
            exit[1] * 2 + 1,
        )

        generator = Generator.create(
            name,
            width,
            height,
            seed,
        )
        generator.generate(
            width,
            height,
            internal_entry,
            internal_exit,
            pattern,
            seed,
        )

        output = Generator.binary_to_hexa(
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
            algorithm=name.strip().lower(),
            seed=generator.get_seed(),
            perfect=True,
            pattern=generator.get_pattern(),
            pattern_cells=generator.get_pattern_cells(),
        )
