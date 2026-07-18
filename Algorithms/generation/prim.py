# from functools import cached_property
from typing import Any
# import numpy as nu
from Algorithms.generation.maze_generator import MazeGenerator


# ** Prim's Algorithm **
#
# The idea: maintain a "frontier" of wall-cells adjacent to the maze-so-far.
# Repeatedly pick one at random, connect it to a random already-visited
# neighbor, then add its neighbors to the frontier.

class Prim(MazeGenerator):
    def __init__(self, width: int, height: int,
                 seed: int | None = None) -> None:
        super().__init__(width, height, seed)

    def generate(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int],
                 pattern: tuple[tuple[Any, ...], ...] | None,
                 seed: int | None, perfect: bool = True) -> None:
        """Generate a maze using randomized Prim's algorithm."""
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.record: list[list[int]] = []
        self.pattern = None
        # Fill the maze with 1
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        # self.maze[0][0] = 0
        self.lock_pattern(pattern, entry, exit)
        # Initiate the path generating
        # start_x: int = entry[0]
        # start_y: int = entry[1]
        # self.maze[start_y][start_x] = 0
        start_x, start_y = entry
        self.open_path(start_x, start_y)

        frontier: list[tuple[int, int]] = []

        # ! Doesn't Work with entry even numbers.
        # if not start_x % 2:
        #    start_x += 1
        #    if start_x == self.width:
        #        start_x -= 2

        # if not start_y % 2:
        #    start_y += 1
        #    if start_y == self.height:
        #        start_y -= 2

        self._add_frontier(start_x, start_y, frontier)

        while frontier:
            index = self._random.randrange(len(frontier))
            frontier_x, frontier_y = frontier.pop(index)

            neighbors = self._in_maze_neighbors(
                frontier_x,
                frontier_y,
            )

            if not neighbors:
                continue

            neighbor_x, neighbor_y = self._random.choice(neighbors)

            wall_x = (frontier_x + neighbor_x) // 2
            wall_y = (frontier_y + neighbor_y) // 2

            self.open_path(wall_x, wall_y)
            self.open_path(frontier_x, frontier_y)

            self.record.append([wall_x, wall_y])
            self.record.append([frontier_x, frontier_y])

            self._add_frontier(
                frontier_x,
                frontier_y,
                frontier,
            )
            if not self.perfect:
                self.braid(0.03, "dead_end")

        # while frontier:
        #     # Pick a random frontier cell
        #     idx = self._random.randrange(len(frontier))
        #     fx, fy = frontier.pop(idx)

        #     # Connect it to a random already-open neighbor
        #     neighbors = self._in_maze_neighbors(fx, fy)
        #     if neighbors:
        #         nx, ny = self._random.choice(neighbors)
        #         wx, wy = (fx + nx) // 2, (fy + ny) // 2
        #         self.maze[wy][wx] = 0   # knock down the wall between them
        #         self.maze[fy][fx] = 0   # open the frontier cell itself
        #         self.record.append([wx, wy])
        #         self.record.append([fx, fy])

        #         # Its unvisited neighbors become new frontier
        #         self._add_frontier(fx, fy, frontier)

        # return super().generate(width, height)

    def _add_frontier(self, cx: int, cy: int,
                      frontier: list[tuple[int, int]]) -> None:
        """ Add unvisited neighbors of (cx, cy) to the frontier list """
        # Create next position.
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:

            nx, ny = cx + dx, cy + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if (nx, ny) in self._locked:
                continue
            if self.maze[ny][nx] != 1:
                continue
            if (nx, ny) in frontier:
                continue
            frontier.append((nx, ny))

    def _in_maze_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """ Return neighbors of (x, y) that are already part of the maze """
        result = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height
                    and self.maze[ny][nx] == 0):
                result.append((nx, ny))
        return result
