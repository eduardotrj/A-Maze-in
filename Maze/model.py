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
        self._rows = rows
        self._height: int = len(rows)
        self._width: int = len(rows[0])
        self._entry = entry
        self._exit = exit
        self._seed = seed
        self._perfect = perfect
        self._pattern = pattern

    def cell(self, x, y) -> int:
        """ Return the information in that cell """
        return self._rows[y][x]

    def get_entry(self) -> tuple[int, int]:
        return self._entry

    def get_exit(self) -> tuple[int, int]:
        return self._exit

    def get_seed(self) -> int:
        return self._seed

    def set_pattern(self, pattern) -> None:
        # By string or by quantity of rows?
        self._pattern = pattern

    def get_pattern(self):
        return self._pattern

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

# ? Maybe add a method to convert from perfect to imperfect here?
