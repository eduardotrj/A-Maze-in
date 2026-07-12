import Algorithms.generation.recursive_backtracker as rb
from Maze.model import Maze


class GeneratorFactory:
    """ Manage Maze generators """
    def __init__(self, width: int, height: int, seed=None):
        self.width = width
        self.height = height
        self.seed = seed
        self.generator = rb.Backtracker(width, height, seed)

    @staticmethod
    def create(name, seed=None):
        """ Select the algorithm to generate a maze """

        generators = {
            "recursive_backtraker": rb.Backtracker,
            #"prim": PrimGenerator,
            #"dfs": RecursiveBacktracker,
            #"kruskal": KruskalGenerator
        }
        if name in generators:
            return generators[name](seed=seed)
        else:
            # ? Create a default value in case not any selected???
            raise ValueError(f"Uknown GEnerator Name {name}")

        #return generators[name]()

    @staticmethod
    def generate_maze(width: int, height: int, seed=None):
        """ Call Algorithm to generate a Maze """
        generator = rb.Backtracker(width, height, seed)
        generator.generate(width, height)
        return generator.get_maze()
