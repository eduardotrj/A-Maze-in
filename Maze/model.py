#   from typing import Any


class Maze:
    """ Keep the data of the current Maze generated """

    def __init__(
            self,
            rows: tuple[tuple[int]],
            entry: tuple[int, int],
            exit: tuple[int, int],
            seed: int,
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

    def cell(self, x, y) -> int:
        """ Return the information in that cell """
        return self.rows[y][x]

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
