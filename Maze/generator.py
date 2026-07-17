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
    """ Manage Maze generators """
    _generators: Dict[str, Type[MazeGenerator]] = {
        "recursive_backtraker": rb.Backtracker,
        "krugal": kr.Kruskal,
        "prim": pr.Prim
        # "dfs": RecursiveBacktracker,
        # "kruskal": KruskalGenerator
    }

    def __init__(self, width: int, height: int, seed=None):
        self.width = width
        self.height = height
        self.seed = seed
        # For default value
        # self.generator = rb.Backtracker(width, height, seed)

    @classmethod
    def list_generators(cls) -> list[str]:
        """ Return the list of available Algorithms """
        return sorted(cls._generators.keys())

    @staticmethod
    def create(name: str, width: int, height: int, seed=None) -> MazeGenerator:
        """ Select the algorithm to generate a maze """
        generator_cls = Generator._generators.get(name)
        if generator_cls is None:
            available = ", ".join(Generator.list_generators())

            raise ValueError(f"Uknown GEnerator Name {name}."
                             f" Available: {available}")

        #   return generators[name]()
        return generator_cls(width, height, seed)

    @staticmethod
    def binary_to_hexa(maze: list[list[int]]) -> list[str]:
        """ Convert binary map in 4-bit wall bitmask """
        NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

        height = len(maze)
        width = len(maze[0])

        # Design logical cells
        rows = range(1, height, 2)
        cols = range(1, width, 2)

        hex_rows = []
        for row in rows:
            line = []
            for col in cols:
                mask = 0
                # Check neighbors
                if col > 0 and col < width:
                    if maze[row][col + 1] == 1:
                        mask |= EAST
                    if maze[row][col - 1] == 1:
                        mask |= WEST

                if row > 0 and row < height:
                    if maze[row - 1][col] == 1:
                        mask |= NORTH

                    if maze[row + 1][col] == 1:
                        mask |= SOUTH

                line.append(mask)
                #   line.append(format(mask, 'x'))
            #   hex_rows.append(''.join(line))
            hex_rows.append(line)
        return hex_rows

    # ! Doesn't translate properly not square

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
        generator = Generator.create(name, width, height, seed)
        generator.generate(width, height, internal_entry, internal_exit,
                           pattern, seed)
        rows = generator.get_maze()
        end_seed: int = generator.get_seed()
        record: list[list[int]] = generator.get_record()
        maze_rows = list(list(row) for row in rows)
        this_pattern = generator.get_pattern()
        pattern_cells = generator.get_pattern_cells()

        # open_cells = [
        #    (x, y)
        #    for y, row in enumerate(rows)
        #    for x, value in enumerate(row)
        #    if value == 0
        # ]
        # entry = open_cells[0] if open_cells else (0, 0)
        # exit = open_cells[-1] if open_cells else (width - 1, height - 1)

        maze_rows = [list(row) for row in rows]
        output = Generator.binary_to_hexa(maze_rows)
        # print("SEED: ", end_seed)
        # print(entry)
        # print(exit)
        return Maze(tuple(output), entry, exit, record, name,
                    end_seed, True, this_pattern, pattern_cells)


# ! Check for of bound specially for odd size maze numbers.
