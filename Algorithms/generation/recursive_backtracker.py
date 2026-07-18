from typing import Any
import sys
from Algorithms.generation.maze_generator import MazeGenerator

sys.setrecursionlimit(10**6)


class Backtracker(MazeGenerator):
    """Generate a maze using recursive backtracking."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
    ) -> None:
        super().__init__(width, height, seed)

    def generate(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        pattern: tuple[tuple[Any], ...] | None,
        seed: int | None,
        perfect: bool = True
    ) -> None:
        """Generate a maze with recursive backtracking."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.record = []
        self.maze = [
            [1 for _ in range(width)]
            for _ in range(height)
        ]

        self.lock_pattern(pattern, entry, exit)

        start_x, start_y = entry
        self.open_path(start_x, start_y)
        self.record.append([start_x, start_y])

        self._carve_passages_from(start_x, start_y)

        if not self.perfect:
            self.braid(0.2, "random")

    def _carve_passages_from(self, x: int, y: int) -> None:
        """Carve passages recursively from the current cell."""
        directions = [
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2),
        ]
        self._random.shuffle(directions)

        for dx, dy in directions:
            next_x = x + dx
            next_y = y + dy
            wall_x = x + dx // 2
            wall_y = y + dy // 2

            if not (
                0 < next_x < self.width - 1
                and 0 < next_y < self.height - 1
            ):
                continue

            if (next_x, next_y) in self._locked:
                continue

            if self.maze[next_y][next_x] != 1:
                continue

            self.open_path(wall_x, wall_y)
            self.open_path(next_x, next_y)

            self.record.append([wall_x, wall_y])
            self.record.append([next_x, next_y])

            self._carve_passages_from(next_x, next_y)
