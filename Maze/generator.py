
# from algorithms.maze_generator import

class GeneratorFactory:
    """ Manage Maze generators """

    @staticmethod
    def create(name):

        generators = {

            "prim": PrimGenerator,
            "dfs": RecursiveBacktracker,
            "kruskal": KruskalGenerator
        }

        return generators[name]()
