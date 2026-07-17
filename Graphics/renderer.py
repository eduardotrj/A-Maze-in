from abc import ABC, abstractmethod
import numpy as np
#import cv2
import time
from Graphics.theme import ThemeManager
from Utils.constants import Tile, HexaWall, WALL_SEGMENTS
# from Maze.patterns import PATTERN


# Working process:
# Renderer -> Canvas -> MiniLibx
# Window -> EventManager -> MiniLibx

#   renderer.draw(grid)
class Renderer(ABC):
    """
    Convert data into Graphics

    """

    @abstractmethod
    def draw(self, obj, any) -> None:
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
        # self.theme = 'default'
        self.animated = False
        self.theme = ThemeManager(self.canvas, self.tile_size)
#        # Load Graphics:\

    def new_theme(self, theme) -> None:
        self.theme.set_theme(theme)

    def draw(self, maze, animation: bool) -> None:
        """ Call others Draw() Methods in orden """
        # 1. Background.\
        # 2. Fill area.\
        # 3. Put external Wall
        self.canvas.clear(self.window)
        self.draw_grid(maze)
        # 5. put enter/exit

        # If Animation
        if animation:
            self.full_with_walls(maze)
            self.draw_pointers(maze)
            self.draw_animation(maze)
            # if maze.pattern:
            # self.draw_marks(maze)

        else:
            # Load in a screen:
            self.draw_pointers(maze)
            self.draw_maze(maze)

        self.draw_marks(maze)
        # 4. Print inner maze
        # if maze.pattern:
        #     self.draw_marks(maze)

        # 6. Put markets
        print("Renderer: Drawing maze ")

    def draw_grid(self, maze) -> None:
        """ Draw the grid surrounded by a wall """
        # ? Can separate walls from bg for animation.
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

    def full_with_walls(self, maze) -> None:
        """ Full the screen with walls """
        # img = self.theme.get_image(Tile.WALL)

        self.canvas.clean_buffer()

        for y in range(1, maze.height * 2 + 1):
            for x in range(1, maze.width * 2 + 1):
                img_arr = self.theme.get_img_raw(Tile.WALL)

                y_start = y * self.tile_size
                y_end = y_start + self.tile_size
                x_start = x * self.tile_size
                x_end = x_start + self.tile_size

                # Copy the tile + position into MLX window memory
                self.canvas.copy_to_buffer(y_start, y_end, x_start, x_end,
                                           img_arr)

        self.canvas.print_screen(0, 0)

    def draw_animation(self, maze) -> None:
        """ Draw the grid with the maze cells """
        # FULL with walls
        # Draw paths by order
        entry_x = maze.entry[0] * 2 + 1
        entry_y = maze.entry[1] * 2 + 1
        exit_x = maze.exit[0] * 2 + 1
        exit_y = maze.exit[1] * 2 + 1
        for step in maze.record:
            self.canvas.syncro()
            # Avoid step over start and exit points
            if not (((entry_x == step[0]) and (entry_y == step[1]))
                    or ((exit_x == step[0]) and (exit_y == step[1]))):
                self.draw_cell(
                            step[0] - 1,
                            step[1] - 1,
                            self.theme.get_image(Tile.PATH)     # hexadecimal n
                        )

    def draw_maze(self, maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                # time.sleep(0.1)
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
        # screen_x = (x * tile)
        # screen_y = (y * tile)
        self.canvas.syncro()
        for direction, offsets in WALL_SEGMENTS.items():
            if cell & direction:
                for dx, dy in offsets:
                    self.draw_cell(x + dx, y + dy, wall)

    def draw_pointers(self, maze) -> None:
        self.canvas.syncro()
        self.draw_cell(
            maze.entry[0] * 2,
            maze.entry[1] * 2,
            self.theme.get_image(Tile.START)
        )
        self.draw_cell(
            (maze.exit[0] * 2),
            (maze.exit[1] * 2),
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

    def draw_marks(self, maze) -> None:
        """Draw the visual marker of actual closed pattern cells."""
        mark = self.theme.get_image(Tile.MARK)

        for x, y in maze.pattern_cells:
            self.draw_cell(
                x * 2,
                y * 2,
                mark,
            )
        # """ Fill the core of the Pattern """
        # # px, py = int((maze.width + 2) / 2), int((maze.height + 2) / 2)
        # # py: int = (maze.height - len(PATTERN["CORE"])) // 2 + 4
        # # px: int = (maze.width - len(PATTERN["CORE"][0])) // 2 + 4

        # def position(side: int, p_size: int):
        #     print(f"Side: {side}, Pattern: {p_size}")
        #     pos = side - int(p_size / 2)
        #     if pos % 2:
        #         pos -= 1
        #     return max(pos, 1)

        # pos_x = position(maze.width, len(PATTERN["CORE"][0]))
        # pos_y = position(maze.height, len(PATTERN["CORE"]))

        # for dy, row in enumerate(PATTERN["CORE"]):
        #     for dx, value in enumerate(row):
        #         if value == 'X':
        #             self.draw_cell(
        #                 pos_x + dx + 1,
        #                 pos_y + dy - 1,
        #                 self.theme.get_image(Tile.MARK)
        #             )

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


"""
50 -> 43
40 -> 33
36 -> 29
30 -> 23
28 -> 22
25 -> 17
23 -> 15
22 -> 15
20 -> 13
19 -> 11
18 -> 11
17 -> 9
16 -> 9
15 -> 7
14 -> 7
12 -> 5
10 -> 3
9 -> 1
8 -> 1

remove 8, add 1

width - 8
"""
