from functools import lru_cache
from typing import Any
import numpy as nu
import sys
from Algorithms.generation.maze_generator import MazeGenerator
from Maze.patterns import PATTERN

# ** RECURSIVE BACKTRACKER **
# Selet a random cell as starting point.
# Choose random adjacent cell -> Create a passage if is free.
# When is not more adjacent free cell. Return until when is.
# When return to start point -> No more free cells = Done


class Backtracker(MazeGenerator):
    def __init__(self, width: int, height: int, seed: int = None):
        super().__init__(width, height, seed)

    def generate(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], pattern: tuple[tuple[Any]] | None,
                 seed: int | None) -> None:
        """ Generate a maze with the given width and height """
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.record: list[list[int]] = []
        self.pattern = None
        # Fill the maze with 1
        self.maze = [[1 for _ in range(width)] for _ in range(height)]

        # Lock Pattern
        self._locked = set()
        if pattern is not None:
            # Doesn't work properly
            # py: int = (width - len(pattern)) // 2
            # px: int = (height - len(pattern[0])) // 2
            try:
                px, py = int(width / 2 - 6), int(height / 2 - 6)
                self._locked = self.validate_pattern(px, py, self.entry,
                                                     self.exit, pattern)
                # Forced only one pattern to avoid Graphic problems.
                self.pattern = PATTERN["CORE"]
            except ValueError as e:
                sys.stderr.write(f"Pattern Problem {e}")
            self.pattern = None

        # Initiate the path generating
        # self.maze[self.exit[0]][self.exit[1]] = 0
        self._carve_passages_from(self.entry[0], self.entry[1])
        for dy, row in enumerate(PATTERN["C42"]):
            for dx, value in enumerate(row):

                # self.maze[dy][dx] = value
                if value == ' ' or 0:
                    self.record.append([dx + px, dy + py])

        # if self.pattern is not None:
        #    self._connect_pattern()

    @lru_cache(maxsize=None)
    def _carve_passages_from(self, cx: int, cy: int):
        """ Create Passages and fill the mase using recursive backtracking """
        # Create possible movements.
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        self._random.shuffle(directions)

        # If entry pos is even, the data became corrupted then:
        if not cx % 2:
            cx += 1
            if cx == self.width:
                cx -= 2

        if not cy % 2:
            cy += 1
            if cy == self.height:
                cy -= 2

        for dx, dy in directions:
            # Draw the next movement randomly
            nx, ny = cx + dx, cy + dy
            wx, wy, = cx + dx // 2, cy + dy // 2

            # Check viability of next movement.
            if (0 < nx < self.width
               and 0 <= ny < self.height
               and self.maze[ny][nx] == 1
               and (nx, ny) not in self._locked
               and (wx, wy) not in self._locked):
                # Connect both cells
                # self.open_path(cy + dy // 2, cx + dx // 2)
                posx = cx + dx // 2
                posy = cy + dy // 2
                self.maze[posy][posx] = 0
                self.record.append([posx, posy])
                # Open next cell
                self.maze[ny][nx] = 0
                self.record.append([nx, ny])
                # self.open_path(ny, nx) # ! Check the values are opposite to open/clsoe (0, 1)
                # Predict next position by recursive
                self._carve_passages_from(nx, ny)

    def _connect_pattern(self):
        """ Connect open spaces between pattern and rest of the maze """
        for (x, y) in self._locked:
            if self.maze[y][x] != 0:
                continue
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                   and (nx, ny) not in self._locked):
                    self.maze[ny][nx] = 0
                    self.record.append([nx, ny])
                    break

    def get_maze(self):
        """ Return the generated maze """
        for x in self.maze:
            print(x)
        return super().get_maze()
