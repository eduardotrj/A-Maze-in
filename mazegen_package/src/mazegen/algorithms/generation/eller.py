from typing import Any
from .maze_generator import MazeGenerator


class Eller(MazeGenerator):
    """ Generate mazes by rows and connecting it """
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
        """ Generate a maze using Eller's algorithm
        (row by row, no recursion) """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.record = []
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        self.lock_pattern(pattern, entry, exit)

        num_cols = (width - 1) // 2
        num_rows = (height - 1) // 2

        # Open every logical cell up front
        for j in range(num_rows):
            for i in range(num_cols):
                x, y = 1 + 2 * i, 1 + 2 * j
                if (x, y) not in self._locked:
                    self.maze[y][x] = 0
                    self.record.append([x, y])

        row_sets = list(range(num_cols))   # each cell starts in its own set
        self._next_set_id = num_cols

        # Save last row to know when ends each stage
        for j in range(num_rows):
            y = 1 + 2 * j
            is_last_row = (j == num_rows - 1)

            # Randomly join horizontally-adjacent cells in different sets
            for i in range(num_cols - 1):
                x = 1 + 2 * i
                if (x, y) in self._locked or (x + 2, y) in self._locked:
                    continue
                if row_sets[i] == row_sets[i + 1]:
                    continue
                if is_last_row or self._random.random() < 0.5:
                    wx, wy = x + 1, y
                    if (wx, wy) in self._locked:
                        continue
                    self.maze[wy][wx] = 0
                    self.record.append([wx, wy])
                    self._merge_sets(row_sets, row_sets[i + 1], row_sets[i])

            # When is the last, move to the next stage
            if is_last_row:
                break

            #  Carve at least one vertical connection per set into next nx row
            groups: dict[int, list[int]] = {}
            for i, s in enumerate(row_sets):
                groups.setdefault(s, []).append(i)

            next_row_sets: list[Any] = [None] * num_cols
            for s, indices in groups.items():
                self._random.shuffle(indices)
                count = self._random.randint(1, len(indices))
                for i in indices[:count]:
                    x = 1 + 2 * i
                    if (x, y) in self._locked or (x, y + 2) in self._locked:
                        continue
                    wx, wy = x, y + 1
                    if (wx, wy) in self._locked:
                        continue
                    self.maze[wy][wx] = 0
                    self.record.append([wx, wy])
                    next_row_sets[i] = s

            # Reset any cell with not verticall connections -.> Soluble
            for i in range(num_cols):
                if next_row_sets[i] is None:
                    next_row_sets[i] = self._next_set_id
                    self._next_set_id += 1

            row_sets = next_row_sets

            #  locked cell in a row currently corrupt union/connection logic
            #  By default needs to open a path to increase options.
            if not self.perfect:
                self.braid(0.1, "dead_end")
            elif pattern:
                self.braid(0.06, "dead_end")

    def _merge_sets(self, row_sets: list[int], old: int, new: int) -> None:
        """ Relabel every cell belonging to `old` as `new` """
        for k in range(len(row_sets)):
            if row_sets[k] == old:
                row_sets[k] = new
