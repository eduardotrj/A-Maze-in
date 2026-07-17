from abc import ABC, abstractmethod
from typing import Any
import random
import secrets


class MazeGenerator(ABC):
    """ Root Design for any Maze Generator Algorithm """
    @abstractmethod
    def __init__(self, width: int, height: int,
                 seed=None) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        self.seed = seed
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        if self.seed == None:
            self.generate_seed()
        self._random = random.Random(seed)
        self.record: list[list[int]]
        self.pattern: tuple[tuple[Any], ...] | None = None

    @abstractmethod
    def generate(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], pattern: tuple[tuple[Any]] | None,
                 seed: int | None) -> None:
        """ Generate a maze with the given width and height """
        pass

    def generate_seed(self) -> None:
        """ Generate a new seed by using secrets (low ratio for repeat) """
        self.seed = secrets.randbits(64)

    def get_maze(self) -> list[list[int]]:
        """ Return the generated Maze """
        return self.maze

    def get_seed(self) -> int:
        return self.seed
    
    def get_pattern(self) -> tuple[tuple[Any], ...] | None:
        return self.pattern

    def get_points(self) -> tuple[tuple[int, int], ...]:
        """ Return Entry and Exit points"""
        return (self.entry, self.exit)

    def get_dimensions(self) -> tuple[int, int]:
        """ Return the dimensions fo the maze """
        return self.width, self.height

    def get_record(self) -> list[list[int]]:
        return self.record

    def get_cell(self, x: int, y: int) -> int:
        """ Return the cell in these coordenates """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.maze[y][x]
        else:
            raise IndexError("Cell coordinates out of bounds")

    def set_cell(self, x: int, y: int, value) -> None:
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

    def space_for_pattern(self, pattern, x: int, y: int) -> bool:
        """ Check if is space enough for the pattern in the maze """
        for dy, row in enumerate(pattern):
            for dx, values in enumerate(row):

                if not (0 <= x + dx < self.width
                        and 0 <= y + dy < self.height):
                    return False

                if self.get_cell(x + dx, y + dy) != 1:
                    return False

        return True

    def not_pointers(self, pattern, x: int, y: int,
                     entry: tuple[int, int], exit: tuple[int, int]):
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

    def validate_pattern(self, x, y, entry: tuple[int, int], exit: tuple[int, int],
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
                    pattern: list[list[int]]):  # -> set[tuple[int, int]]:
        """ Add pattern at the coordenates """

        for dy, row in enumerate(pattern):
            for dx, value in enumerate(row):

                # self.maze[dy][dx] = value
                if value == 1:
                    self.close_path(x + dx, y + dy)
                else:
                    self.open_path(x + dx, y + dy)
