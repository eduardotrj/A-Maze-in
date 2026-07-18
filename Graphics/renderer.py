from abc import ABC, abstractmethod
# import numpy as np
# import cv2
# import time
# from typing import Literal
from typing import Any
from Graphics.theme import ThemeManager
# from Utils.constants import Tile, HexaWall, WALL_SEGMENTS
# from Maze.patterns import PATTERN
from Maze.model import Maze
from Utils.constants import (
    DIRECTIONS,
    OPPOSITE_DIRECTION,
    SOLUTION_TILES,
    # HexaWall,
    Tile,
    WALL_SEGMENTS,
)


# Working process:
# Renderer -> Canvas -> MiniLibx
# Window -> EventManager -> MiniLibx

#   renderer.draw(grid)
class Renderer(ABC):
    """
    Convert data into Graphics

    """

    @abstractmethod
    def draw(self, obj: Any, any: Any) -> None:
        """ Call others Draw() Methods in orden """
        pass

    @abstractmethod
    def draw_grid(self, maze: Maze) -> None:
        """ Draw the grid with the elements """
        pass

    @abstractmethod
    def draw_cell(self, x: Any, y: Any, img_tile: Any) -> None:
        """ Print each cell """
        pass

    @abstractmethod
    def draw_solution(
        self,
        maze: Maze,
        path: str,
    ) -> None:
        """Draw the solution path."""
        pass


class MazeRenderer(Renderer):
    """
    Render a Maze
    """
    def __init__(self, window: Any, canvas: Any, size: int = 32) -> None:
        self.window = window
        self.tile_size = size   # Pixel size
        self.canvas = canvas    # To print into MiniLibx
        # self.theme = 'default'
        self.animated = False
        self.theme = ThemeManager(self.canvas, self.tile_size)
#        # Load Graphics:\

    def new_theme(self, theme: Any) -> None:
        self.theme.set_theme(theme)

    def draw(self, maze: Maze, animation: bool) -> None:
        """ Call others Draw() Methods in orden """
        # 1. Background.\
        # 2. Fill area.\
        # 3. Put external Wall
        self.canvas.clear(self.window)
        self.animated = animation

        # If Animation
        if animation:
            self.draw_grid(maze)
            self.full_with_walls(maze)
            self.draw_pointers(maze)
            self.draw_animation(maze)

        else:
            self.load_full_screen(maze)

        self.draw_marks(maze)

    def draw_grid(self, maze: Maze) -> None:
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

    def load_full_screen(self, maze: Maze) -> None:
        """ Load of the map to print at once """
        self.canvas.clean_buffer()

        # 1. Draw Paths, Start, and Exit tiles
        for y in range(1, maze.height * 2):
            for x in range(1, maze.width * 2):
                if (x == maze.entry[0] * 2 + 1 and y == maze.entry[1] * 2 + 1):
                    img_arr = self.theme.get_img_raw(Tile.START)
                elif (x == maze.exit[0] * 2 + 1 and y == maze.exit[1] * 2 + 1):
                    img_arr = self.theme.get_img_raw(Tile.EXIT)
                else:
                    img_arr = self.theme.get_img_raw(Tile.PATH)

                y_start = y * self.tile_size
                y_end = y_start + self.tile_size
                x_start = x * self.tile_size
                x_end = x_start + self.tile_size

                self.canvas.copy_to_buffer(y_start,
                                           y_end,
                                           x_start,
                                           x_end,
                                           img_arr)

        # 2. Draw Walls safely
        for y in range(0, maze.height):
            for x in range(0, maze.width):

                # FIXED: Loop through segments first,
                # then apply the conditional check
                for direction, offsets in WALL_SEGMENTS.items():
                    if maze.cell(x, y) & direction:
                        for dx, dy in offsets:
                            img_arr = self.theme.get_img_raw(Tile.WALL)

                            # Shift base coordinate to the expanded center
                            # (x*2 + 1)
                            # before applying the relative offset
                            grid_x = (x * 2 + 1) + dx
                            grid_y = (y * 2 + 1) + dy

                            # Safety boundary check: Skip drawing if
                            # coordinates fall off-screen
                            if grid_x < 0 or grid_y < 0:
                                continue

                            y_start = grid_y * self.tile_size
                            y_end = y_start + self.tile_size
                            x_start = grid_x * self.tile_size
                            x_end = x_start + self.tile_size

                            # Final safety check before attempting
                            # array slice injection
                            if y_start >= 0 and x_start >= 0:
                                self.canvas.copy_to_buffer(y_start,
                                                           y_end,
                                                           x_start,
                                                           x_end,
                                                           img_arr)

        # 3. Blit the unified image frame to the screen layout once
        self.canvas.print_screen(0, 0)

    def full_with_walls(self, maze: Maze) -> None:
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

    def draw_animation(self, maze: Maze) -> None:
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

    def draw_maze(self, maze: Maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                # time.sleep(0.1)
                self.draw_walls(
                    x,
                    y,
                    maze.cell(x, y)     # hexadecimal n
                )

    def draw_walls(self, x: Any, y: Any, cell: Any) -> None:
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

    def draw_pointers(self, maze: Maze) -> None:
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

    def draw_cell(self, x: Any, y: Any, image: Any) -> None:
        """ Printing a till with """
        screen_x = x * self.tile_size + self.tile_size
        screen_y = y * self.tile_size + self.tile_size

        self.canvas.draw_image(
            image,
            screen_x,
            screen_y
        )

    def draw_marks(self, maze: Maze) -> None:
        """Draw the visual marker of actual closed pattern cells."""
        mark = self.theme.get_image(Tile.MARK)

        for x, y in maze.pattern_cells:
            self.draw_cell(
                x * 2,
                y * 2,
                mark,
            )

    def draw_solution(self, maze: Maze, path: str) -> None:
        """Draw a solution path over the maze."""
        connections: dict[tuple[int, int], set[str]] = {}
        steps: list[tuple[tuple[int, int], str]] = []

        # self.canvas.clean_buffer()
        current = maze.entry

        for direction in path:
            if direction not in DIRECTIONS:
                raise ValueError(f"Invalid solution direction: {direction}")

            dx, dy, _ = DIRECTIONS[direction]
            next_position = (current[0] + dx, current[1] + dy)

            connections.setdefault(current, set()).add(direction)
            connections.setdefault(next_position,
                                   set()).add(OPPOSITE_DIRECTION[direction])

            steps.append((current, direction))
            current = next_position

        if current != maze.exit:
            raise ValueError("Solution path does not reach the maze exit")

        self.canvas.syncro()

        # --- 1. Draw the corridors between logical cells ---
        for (x, y), direction in steps:
            dx, dy, _ = DIRECTIONS[direction]

            if dx != 0:
                corridor_tile = Tile.S_EW
            else:
                corridor_tile = Tile.S_NS

            if self.animated:
                self.canvas.syncro()
                self.draw_cell(x * 2 + dx, y * 2 + dy,
                               self.theme.get_image(corridor_tile))
            else:
                # FIXED: Correctly paired x with dx, and y with dy
                y_start = (y * 2 + dy + 1) * self.tile_size
                y_end = y_start + self.tile_size
                x_start = (x * 2 + dx + 1) * self.tile_size
                x_end = x_start + self.tile_size

                img_arr = self.theme.get_img_raw(corridor_tile)
                self.canvas.copy_to_buffer(y_start,
                                           y_end,
                                           x_start,
                                           x_end,
                                           img_arr)

        self.canvas.syncro()
        # --- 2. Draw the turns and straight segments at cell centers ---
        for (x, y), directions in connections.items():
            center_tile = SOLUTION_TILES.get(frozenset(directions))

            if center_tile is None:
                raise ValueError(
                    f"Invalid solution path connection at {(x, y)}: "
                    f"{directions}"
                )

            if self.animated:
                # time.sleep(0.1)
                # FIXED: Restored to original working
                # center placement (x*2, y*2)
                self.draw_cell(x * 2, y * 2, self.theme.get_image(center_tile))
                self.canvas.syncro()
            else:
                # FIXED: Removed the stray dx/dy offsets entirely for centers
                y_start = (y * 2 + 1) * self.tile_size
                y_end = y_start + self.tile_size
                x_start = (x * 2 + 1) * self.tile_size
                x_end = x_start + self.tile_size

                img_arr = self.theme.get_img_raw(center_tile)
                self.canvas.copy_to_buffer(y_start,
                                           y_end,
                                           x_start,
                                           x_end,
                                           img_arr)

        # --- 3. Final Render Step ---
        # FIXED: Blit the buffer exactly ONCE at the end
        # instead of spamming it inside the loops
        if not self.animated:
            self.canvas.print_screen(0, 0)

        # Keep entry and exit graphics above the solution.
        self.draw_pointers(maze)

    def generate_background(self) -> None:
        """ Draw Background for the Maze """
        pass

    def generate_floow(self) -> None:
        """ Draw the floor """
        pass

    def generate_points(self) -> None:
        """ Draw start and End point in the maze """
        pass

    def decoding_data(self) -> None:
        pass
        # 4hex = 9 positions (h * 2 = 1)
