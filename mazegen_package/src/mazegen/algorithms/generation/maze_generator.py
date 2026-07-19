from abc import ABC, abstractmethod
from typing import Any
import random
import secrets


class MazeGenerator(ABC):
    """ Root Design for any Maze Generator Algorithm """

    @abstractmethod
    def __init__(self, width: int, height: int,
                 seed: int | None = None) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]

        self.entry: tuple[int, int]
        self.exit: tuple[int, int]

        self.seed = seed
        if self.seed is None:
            self.generate_seed()
        self._random = random.Random(self.seed)

        self.record: list[list[int]]
        self.pattern: tuple[tuple[Any], ...] | None = None
        self._locked: set[tuple[int, int]] = set()
        self.pattern_cells: set[tuple[int, int]] = set()
        self.perfect: bool

    @abstractmethod
    def generate(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int],
                 pattern: tuple[tuple[Any, ...], ...] | None,
                 seed: int | None, perfect: bool = True) -> None:
        """ Generate a maze with the given width and height """
        pass

    def generate_seed(self) -> None:
        """ Generate a new seed by using secrets (low ratio for repeat) """
        self.seed = secrets.randbits(64)

    def get_maze(self) -> list[list[int]]:
        """ Return the generated Maze """
        return self.maze

    def get_seed(self) -> int | None:
        return self.seed

    def get_pattern(self) -> tuple[tuple[Any], ...] | None:
        return self.pattern

    def get_points(self) -> tuple[tuple[int, int], ...]:
        """ Return Entry and Exit points"""
        return (self.entry, self.exit)

    def get_dimensions(self) -> tuple[int, int]:
        """ Return the dimensions fo the maze """
        return self.width, self.height

    def is_perfect(self) -> bool:
        return self.perfect

    def get_record(self) -> list[list[int]]:
        return self.record

    def get_cell(self, x: int, y: int) -> int:
        """ Return the cell in these coordenates """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.maze[y][x]
        else:
            raise IndexError("Cell coordinates out of bounds")

    def set_cell(self, x: int, y: int, value: Any) -> None:
        """ Set the cell at the given coordinates to value"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.maze[y][x] = value
        else:
            raise IndexError("Cell coordinates out of bounds")

    def open_path(self, x: int, y: int) -> None:
        """ Open a path to a given coordenates (set cell to 0) """
        self.set_cell(x, y, 0)

    def close_path(self, x: int, y: int) -> None:
        """ Close a path to a given coordenates (set cell to 1) """
        self.set_cell(x, y, 1)

    def space_for_pattern(self, pattern: Any, x: int, y: int) -> bool:
        """ Check if is space enough for the pattern in the maze """
        for dy, row in enumerate(pattern):
            for dx, values in enumerate(row):

                if not (0 <= x + dx < self.width
                        and 0 <= y + dy < self.height):
                    return False

                if self.get_cell(x + dx, y + dy) != 1:
                    return False

        return True

    def not_pointers(self, pattern: Any, x: int, y: int,
                     entry: tuple[int, int], exit: tuple[int, int]) -> bool:
        entry_x, entry_y = entry[0] * 2, entry[1] * 2
        exit_x, exit_y = exit[0] * 2, exit[1] * 2

        for dy, row in enumerate(pattern):
            for dx, values in enumerate(row):

                # Remove to avoid points in any empty space of the pattern
                if values == 0:
                    break

                if (((entry_x == dx + x) and (entry_y == dy + y))
                   or ((exit_x == dx + x) and (exit_y == dy + y))):
                    return False

        return True

    def pattern_to_binary(self, pattern: tuple[tuple[Any]]) -> list[list[int]]:
        """ Convert a designed 'X'/' ' pattern into maze binary
        (1 = wall, 0 = path) """
        return [[1 if cell == 'X' else 0 for cell in row] for row in pattern]

    def validate_pattern(self, x: Any, y: Any, entry: tuple[int, int],
                         exit: tuple[int, int],
                         pattern: tuple[tuple[Any]] | None = None
                         ) -> set[tuple[int, int]]:
        """ Validate pattern, if is valid, add it """

        if not pattern:
            raise ValueError("No Pattern data")

        binary = self.pattern_to_binary(pattern)
        if not self.space_for_pattern(binary, x, y):
            raise ValueError("No enought space for print the pattern")

        # Check if entry or exit are in the pattern:

        if not self.not_pointers(binary, x, y, entry, exit):
            raise ValueError("Start or exit in the pattern area")

        self.add_pattern(x, y, binary)
        return {
            (x + dx, y + dy)
            for dy, row in enumerate(binary)
            for dx, _ in enumerate(row)
        }

    def add_pattern(self, x: int, y: int,
                    pattern: list[list[int]]) -> None:
        """ Add pattern at the coordenates """

        for dy, row in enumerate(pattern):
            for dx, value in enumerate(row):

                # self.maze[dy][dx] = value
                if value == 1:
                    self.close_path(x + dx, y + dy)
                else:
                    self.open_path(x + dx, y + dy)

    def lock_pattern(
        self,
        pattern: tuple[tuple[Any], ...] | None,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Reserve the closed cells used to draw the pattern."""
        self._locked.clear()
        self.pattern_cells.clear()

        if pattern is None:
            return

        logical_width = (self.width - 1) // 2
        logical_height = (self.height - 1) // 2

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        if (
            pattern_width > logical_width
            or pattern_height > logical_height
        ):
            print("Warning: maze is too small for the 42 pattern")
            return

        start_x = (logical_width - pattern_width) // 2
        start_y = (logical_height - pattern_height) // 2

        for dy, row in enumerate(pattern):
            for dx, value in enumerate(row):
                if value != "X":
                    continue

                logical_x = start_x + dx
                logical_y = start_y + dy

                internal_x = logical_x * 2 + 1
                internal_y = logical_y * 2 + 1

                internal_position = (internal_x, internal_y)

                if internal_position in (entry, exit_):
                    #   raise ValueError(
                    #       "Entry or exit overlaps the 42 pattern"
                    #   )
                    print("Warning: Start or exit in the Pattern area.")
                    return

                self.pattern_cells.add((logical_x, logical_y))
                self._locked.add(internal_position)

        self.pattern = pattern

    def get_pattern_cells(self) -> set[tuple[int, int]]:
        """Return logical cells occupied by the pattern."""
        return self.pattern_cells.copy()

    def braid(self, factor: float = 0.1, method: str = "random") -> None:
        """
        Break extra walls to open new paths.

        factor: 0.0-1.0, chance/fraction of candidate walls that get removed
        method: "random"   -> factor chance to any random wall be opened
                "dead_end" -> `factor` fraction of dead-end cells get opened
        """
        locked: set[tuple[int, int]] = getattr(self, "_locked", set())
        if not hasattr(self, "record"):
            self.record = []

        if method == "dead_end":
            self._braid_dead_ends(factor, locked)
        else:
            self._braid_random_walls(factor, locked)

    def _braid_random_walls(self, factor: float,
                            locked: set[tuple[int, int]]) -> None:
        """
        Remove some walls between already-open neighboring cells randomly
        """
        for wy in range(1, self.height - 1):
            for wx in range(1, self.width - 1):
                if self.maze[wy][wx] != 1 or (wx, wy) in locked:
                    continue

                # Check if the wall is between 2 neightbors cells
                if wx % 2 == 0 and wy % 2 == 1:
                    c1, c2 = (wx - 1, wy), (wx + 1, wy)
                elif wx % 2 == 1 and wy % 2 == 0:
                    c1, c2 = (wx, wy - 1), (wx, wy + 1)
                else:
                    continue

                # Check if is in the pattern or out of the maze
                if c1 in locked or c2 in locked:
                    continue
                if not (0 <= c1[0] < self.width and 0 <= c1[1] < self.height):
                    continue

                if not (0 <= c2[0] < self.width and 0 <= c2[1] < self.height):
                    continue

                if (self.maze[c1[1]][c1[0]] == 0
                        and self.maze[c2[1]][c2[0]] == 0
                        and self._random.random() < factor
                        and not self._completes_open_block(wx, wy)):
                    self.maze[wy][wx] = 0
                    self.record.append([wx, wy])

    def _find_dead_ends(self,
                        locked: set[tuple[int, int]]) -> list[tuple[int, int]]:
        """ Return all logical cells with exactly one open connection """
        dead_ends = []
        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                if (x, y) in locked or self.maze[y][x] != 0:
                    continue

                # Count how many apertures have
                open_count = 0
                for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                    nx, ny = x + dx, y + dy
                    wx, wy = x + dx // 2, y + dy // 2
                    if (0 <= nx < self.width and 0 <= ny < self.height
                            and self.maze[wy][wx] == 0):
                        open_count += 1
                # Only open if have only 1
                if open_count == 1:
                    dead_ends.append((x, y))
        return dead_ends

    def _braid_dead_ends(self, factor: float,
                         locked: set[tuple[int, int]]) -> None:
        """
        Remove a fraction of dead ends by opening one extra wall from each
        """
        dead_ends = self._find_dead_ends(locked)
        self._random.shuffle(dead_ends)
        n = int(len(dead_ends) * factor)

        for x, y in dead_ends[:n]:
            candidates = []
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                nx, ny = x + dx, y + dy
                wx, wy = x + dx // 2, y + dy // 2
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and self.maze[wy][wx] == 1
                        and (nx, ny) not in locked and (wx, wy) not in locked
                        and not self._completes_open_block(wx, wy)):
                    candidates.append((wx, wy))
            if candidates:
                wx, wy = self._random.choice(candidates)
                self.maze[wy][wx] = 0
                self.record.append([wx, wy])

    def _completes_open_block(self, wx: int, wy: int) -> bool:
        """
        Check if opening the wall at (wx, wy) would complete a fully-open
        2x2 block of cells (Avoid those ugly open spacesS).
        """
        blocks = []
        # vertical wall: connects left/right cells, wy is odd
        if wx % 2 == 0:
            blocks.append((wx - 1, wy))
            blocks.append((wx - 1, wy - 2))
        # horizontal wall: connects up/down cells, wx is odd
        else:
            blocks.append((wx, wy - 1))
            blocks.append((wx - 2, wy - 1))

        for cx, cy in blocks:
            if not (0 <= cx and cx + 2 < self.width
                    and 0 <= cy and cy + 2 < self.height):
                continue

            cells = [(cx, cy), (cx + 2, cy), (cx, cy + 2), (cx + 2, cy + 2)]
            walls = [(cx + 1, cy), (cx, cy + 1),
                     (cx + 2, cy + 1), (cx + 1, cy + 2)]

            if all(self.maze[y][x] == 0 for x, y in cells) and \
               all(self.maze[y][x] == 0 for x, y in walls
                   if (x, y) != (wx, wy)):
                return True   # the other 3 edges are already open
        return False
