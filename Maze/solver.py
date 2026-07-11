# from algorithms.solver_generator import

class SolverFactory:
    """ Manage solution generators """

    @staticmethod
    def create(name):

        generators = {

            "prim": PrimGenerator,
            "dfs": RecursiveBacktracker,
            "kruskal": KruskalGenerator
        }

        return generators[name]()
