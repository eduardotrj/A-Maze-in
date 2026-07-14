import Algorithms.generation.recursive_backtracker as rb
from Algorithms.generation.maze_generator import MazeGenerator
from Maze.model import Maze
from typing import Dict, Type


class Generator:
    """ Manage Maze generators """
    _generators: Dict[str, Type[MazeGenerator]] = {
        "recursive_backtraker": rb.Backtracker,
        # "prim": PrimGenerator,
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
    
    # ! DOesn't translate properly not square

    @staticmethod
    def generate_maze(width: int,
                      height: int,
                      entry: tuple[int, int],
                      exit: tuple[int, int],
                      name: str = "recursive_backtraker",
                      seed: int | None = None):
        """ Call Algorithm to generate a Maze """
        generator = Generator.create(name, width, height, seed)
        generator.generate(width, height, entry, exit, seed)
        rows = generator.get_maze()
        maze_rows = tuple(tuple(row) for row in rows)

        open_cells = [
            (x, y)
            for y, row in enumerate(rows)
            for x, value in enumerate(row)
            if value == 0
        ]
        entry = open_cells[0] if open_cells else (0, 0)
        exit = open_cells[-1] if open_cells else (width - 1, height - 1)

        output = Generator.binary_to_hexa(maze_rows)

        return Maze(output, entry, exit, seed)


# ! Check for of bound specially for odd size maze numbers.
