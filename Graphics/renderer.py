from Graphics.canvas import MLXCanvas
from abc import ABC, abstractmethod
import numpy as np

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
    def draw_grid(self, maze) -> None:
        """ Draw the grid with the elements """
        pass

    @abstractmethod
    def draw_cell(self, x, y, cell) -> None:
        """ Print each cell """
        pass

    @abstractmethod
    def draw_solution(self, path) -> None:
        pass

class MazeRenderer(Renderer):
    """
    Render a Maze
    """
    def __init__(self, window, size: int = 32) -> None:
        self.window = window
        self.tile_size = size  # Pixel size
        self.canvas = MLXCanvas()  # To print into MiniLibx
        self.theme = 'default'
        # Load Graphics:\
        self.wall = self.gen_array('wall.png')
        self.

    def img_array(self, filename: str, resizing: bool = False) -> np.ndarray:
        """ Transform an img into a data array with BGRA channels """



    def draw(self) -> None:
        """ Call others Draw() Methods in orden """
        print("Renderer: Drawing maze ")

    def draw_grid(self, maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                self.draw_cell(
                    x,
                    y,
                    maze.cell(x, y)     # hexadecimal n
                )
        #   self.canvas.clear()
        #   self.canvas.draw_pixel()

    def draw_cell(self, x, y, cell) -> None:
        NORTH = 0x1
        EAST = 0x2
        SOUTH = 0x4
        WEST = 0x8

        screen_x = x * self.tile_size
        screen_y = y * self.tile_size

        if cell & NORTH:
            self.canvas.draw_image(
                #   self.wall_north,
                self.wall,
                screen_x,
                screen_y
            )

        if cell & EAST:
            self.canvas.draw_image(
                #   self.wall_east,
                self.wall,
                screen_x,
                screen_y
            )

        if cell & SOUTH:
            self.canvas.draw_image(
                #   self.wall_south,
                self.wall,
                screen_x,
                screen_y
            )

        if cell & WEST:
            self.canvas.draw_image(
                #   self.wall_west,
                self.wall,
                screen_x,
                screen_y
            )

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

