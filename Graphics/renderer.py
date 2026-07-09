from Graphics.canvas import MLXCanvas
from abc import ABC, abstractmethod

# Working process:
# Renderer -> Canvas -> MiniLibx
# Window -> EventManager -> MiniLibx


#   renderer.draw(grid)
class Renderer(ABC):
    """
    Convert data into Graphics

    """

    @abstractmethod
    def draw(self) -> None:
        """ Call others Draw() Methods in orden """
        pass

    @abstractmethod
    def draw_grid(self) -> None:
        pass

    @abstractmethod
    def draw_cell(self, cell) -> None:
        pass

    @abstractmethod
    def draw_solution(self, path) -> None:
        pass


class MazeRenderer(Renderer):
    """
    Render a Maze
    """

    def __init__(self, window) -> None:
        self.canvas = MLXCanvas()  # To print into MiniLibx

    def draw(self) -> None:
        """ Call others Draw() Methods in orden """
        print("Renderer: Drawing maze ")

        self.canvas.clear()
        self.canvas.draw_pixel()

    def draw_grid(self) -> None:
        pass

    def draw_cell(self, cell) -> None:
        pass

    def draw_solution(self, path) -> None:
        """ Draw the solution (PATH)"""
        pass

    def generate_background(self) -> None:
        """ Draw Background for the Maze """
        pass

    def generate_walls(self) -> None:
        """ Draw the walls: Originally full all with walls """
        pass

    def generate_floow(self) -> None:
        """ Draw the floor """
        pass

    def generate_points(self) -> None:
        """ Draw start and End point in the maze """
