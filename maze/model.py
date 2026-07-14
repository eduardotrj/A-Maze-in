#   from typing import Any
from utils.constants import DIRECTIONS


class Maze:
    """ Keep the data of the current Maze generated """

    def __init__(
            self,
            rows: tuple[tuple[int, ...], ...],
            entry: tuple[int, int],
            exit: tuple[int, int],
            seed: int | None,
            perfect: bool = True,
            pattern: list[str] | None = None
            ):
        self.rows = rows
        self.height: int = len(rows)
        self.width: int = len(rows[0])
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        self.pattern = pattern

    def cell(self, x: int, y: int) -> int:
        """ Return the information in that cell """
        return self.rows[y][x]

    def get_open_neighbors(
        self,
        position: tuple[int, int],
    ) -> list[tuple[tuple[int, int], str]]:
        """Return all reachable neighboring cells."""
        x, y = position
        cell = self.cell(x, y)

        neighbors: list[tuple[tuple[int, int], str]] = []

        for direction, (dx, dy, wall_bit) in DIRECTIONS.items():
            next_x = x + dx
            next_y = y + dy

            if next_x < 0 or next_x >= self.width:
                continue

            if next_y < 0 or next_y >= self.height:
                continue

            if cell & wall_bit:
                continue

            neighbors.append(((next_x, next_y), direction))

        return neighbors

    #   def get_entry(self) -> tuple[int, int]:
    #       return self._entry

    #   def get_exit(self) -> tuple[int, int]:
    #       return self._exit

    #   def get_seed(self) -> int:
    #       return self._seed

    #   def set_pattern(self, pattern) -> None:
    #       # By string or by quantity of rows?
    #       self._pattern = pattern

    #   def get_pattern(self):
    #       return self._pattern

    #   def get_height(self):
    #       return self._height

    #   def get_width(self):
    #       return self._width

# ? Maybe add a method to convert from perfect to imperfect here?
