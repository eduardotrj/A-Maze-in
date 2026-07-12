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
    def generate_maze(width: int, height: int,
                      name: str = "recursive_backtraker", seed=None):
        """ Call Algorithm to generate a Maze """
        generator = Generator.create(name, width, height, seed)
        generator.generate(width, height)
        rows = generator.get_maze()
        maze_rows = tuple(tuple(row) for row in rows)

        open_cells = [
            (x, y)
            for y, row in enumerate(rows)
            for x, value in enumerate(row)
            if value = 0
        ]
        entry = open_cells[0] if open_cells else (0, 0)
        exit = open_cells[-1] if open_cells else (width - 1, height - 1)

        return Maze(maze_rows, entry, exit, seed)
