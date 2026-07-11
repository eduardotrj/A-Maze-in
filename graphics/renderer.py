from Graphics.canvas import Canvas
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
    Convert data into Graphics

    """

    def __init__(self, window) -> None:
        self.canvas = Canvas()  # To print into MiniLibx

    def draw(self) -> None:
        """ Call others Draw() Methods in orden """
        pass

    def draw_grid(self) -> None:
        pass

    def draw_cell(self, cell) -> None:
        pass

    def draw_solution(self, path) -> None:
        pass
