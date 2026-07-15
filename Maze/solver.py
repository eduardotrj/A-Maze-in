# from algorithms.solver_generator import
from Algorithms.solving.astar import solve_astar
from Algorithms.solving.bfs import solve_bfs
from Algorithms.solving.dfs import solve_dfs
from Algorithms.solving.dijkstra import solve_dijkstra

from Maze.model import Maze


# Edu
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


# Eray
def solve_maze(
    maze: Maze,
    algorithm: str = "bfs",
) -> str | None:
    """Solve a maze using the selected algorithm."""
    solvers = {
        "bfs": solve_bfs,
        "dfs": solve_dfs,
        "astar": solve_astar,
        "dijkstra": solve_dijkstra,
    }

    if algorithm not in solvers:
        raise ValueError(
            f"Unknown solving algorithm: {algorithm}"
        )

    return solvers[algorithm](maze)
