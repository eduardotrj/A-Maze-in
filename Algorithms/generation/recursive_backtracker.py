from functools import cached_property
import numpy as nu
import random
from Algorithms.generation.maze_generator import MazeGenerator

# ** RECURSIVE BACKTRACKER **
# Selet a random cell as starting point.
# Choose random adjacent cell -> Create a passage if is free.
# When is not more adjacent free cell. Return until when is.
# When return to start point -> No more free cells = Done


class Backtracker(MazeGenerator):
    def __init__(self, width: int, height: int, seed: int = None):
        super().__init__(width, height, seed)
        self.maze

    def generate(self, width: int, height: int):
        """ Generate a maze with the given width and height """
        self.width = width
        self.height = height
        # Fill the maze with 1
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        # Initiate the path generating
        self._carve_passages_from(0, 0)

    @cached_property
    def _carve_passages_from(self, cx: int, cy: int):
        """ Create Passages and fill the mase using recursive backtracking """
        # Create possible movements.
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        # ? Add here a recorder to printing animation????
        for dx, dy in directions:
            # Draw the next movement randomly
            nx, ny = cx + dx, cy + dy

            # Check viability of next movement.
            if (0 <= nx < self.width and 0 <= ny < self.height
               and self.maze[ny][nx] == 1):
                # Open next cell
                self.open_path(ny, nx)
                # Connect both cells
                self.open_path(cy + dy // 2, cx + dx // 2)
                # Predict next position by recursive
                self._carve_passages_from(nx, ny)

    def get_maze(self):
        """ Return the generated maze """
        return super().get_maze()
