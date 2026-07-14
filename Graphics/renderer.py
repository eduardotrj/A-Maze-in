from abc import ABC, abstractmethod
import numpy as np
#import cv2
import time
from Graphics.theme import ThemeManager
from Utils.constants import Tile, HexaWall, WALL_SEGMENTS


# Working process:
# Renderer -> Canvas -> MiniLibx
# Window -> EventManager -> MiniLibx

#   renderer.draw(grid)
class Renderer(ABC):
    """
    Convert data into Graphics

    """

    @abstractmethod
    def draw(self, obj) -> None:
        """ Call others Draw() Methods in orden """
        pass

    @abstractmethod
    def draw_grid(self, maze) -> None:
        """ Draw the grid with the elements """
        pass

    @abstractmethod
    def draw_cell(self, x, y, img_tile) -> None:
        """ Print each cell """
        pass

    @abstractmethod
    def draw_solution(self, path) -> None:
        pass


class MazeRenderer(Renderer):
    """
    Render a Maze
    """
    def __init__(self, window, canvas, size: int = 32) -> None:
        self.window = window
        self.tile_size = size   # Pixel size
        self.canvas = canvas    # To print into MiniLibx
        #self.theme = 'default'
        self.animated = False
        self.theme = ThemeManager(self.canvas, self.tile_size)
#        # Load Graphics:\

    def new_theme(self, theme) -> None:
        self.theme.set_theme(theme)

    def draw(self, maze) -> None:
        """ Call others Draw() Methods in orden """
        # 1. Background.\
        # 2. Fill area.\
        # 3. Put external Wall
        self.canvas.clear(self.window)
        self.draw_grid(maze)
        # 5. put enter/exit

        # If Animation
        #self.full_with_walls(maze)
        self.draw_pointers(maze)
        #self.draw_animation(maze)

        # 4. Print inner maze
        self.draw_maze(maze)
        
        # 6. Put markets
        print("Renderer: Drawing maze ")

    def draw_grid(self, maze) -> None:
        """ Draw the grid surrounded by a wall """
        #? Can separate walls from bg for animation.
        max_height = maze.height * 2
        max_width = maze.width * 2

        # Maze not located in 00. require -1 to full frame filling
        for y in range(-1, max_height):
            self.canvas.syncro()
            for x in range(-1, max_width):
                if (y == -1 or y == (max_height - 1)):
                    self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.WALL)    # hexadecimal n
                    )
                elif (x == -1 or x == (max_width - 1)):
                    self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.WALL)     # hexadecimal n
                    )
                else:
                    self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.PATH)     # hexadecimal n
                    )
        #   self.canvas.clear()
        #   self.canvas.draw_pixel()

    def full_with_walls(self, maze) -> None:
        for y in range(maze.height * 2 + 1):
            for x in range(maze.width * 2 + 1):
                self.canvas.syncro()
                self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.WALL)     # hexadecimal n
                    )
                
    def draw_animation(self, maze) -> None:
        """ Draw the grid with the maze cells """
        # FULL with walls
        # Draw paths by order
        for step in maze.record:
            self.canvas.syncro()
            self.draw_cell(
                        step[0] - 1,
                        step[1] - 1,
                        self.theme.get_image(Tile.PATH)     # hexadecimal n
                    )

    def draw_maze(self, maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                #time.sleep(0.1)
                self.draw_walls(
                    x,
                    y,
                    maze.cell(x, y)     # hexadecimal n
                )

    def draw_walls(self, x, y, cell) -> None:
        """ Logic to draw the different walls in the maze"""
        x *= 2
        y *= 2
        wall = self.theme.get_image(Tile.WALL)

        # Printing in the center
        #screen_x = (x * tile)
        #screen_y = (y * tile)
        self.canvas.syncro()
        for direction, offsets in WALL_SEGMENTS.items():
            if cell & direction:
                for dx, dy in offsets:
                    self.draw_cell(x + dx, y + dy, wall)

    def draw_pointers(self, maze) -> None:
        self.canvas.syncro()
        self.draw_cell(
            maze.entry[0] * 2 - 2,
            maze.entry[1] * 2 - 2,
            self.theme.get_image(Tile.START)
        )
        self.draw_cell(
            (maze.exit[0] * 2 - 2),
            (maze.exit[1] * 2 - 2),
            self.theme.get_image(Tile.EXIT)
        )

    def draw_cell(self, x, y, image) -> None:
        """ Printing a till with """
        screen_x = x * self.tile_size + self.tile_size
        screen_y = y * self.tile_size + self.tile_size

        self.canvas.draw_image(
            image,
            screen_x,
            screen_y
        )

    def draw_solution(self, path) -> None:
        """ Draw the solution (PATH)"""
        pass

    def generate_background(self) -> None:
        """ Draw Background for the Maze """
        pass

    def generate_floow(self) -> None:
        """ Draw the floor """
        pass

    def generate_points(self) -> None:
        """ Draw start and End point in the maze """
        pass

    def decoding_data(self):
        pass
        # 4hex = 9 positions (h * 2 = 1)
