from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    
    @abstractmethod
    def __init__(self, width: int, height: int, seed=None) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.maze = None
        self.seed = seed

    @abstractmethod
    def generate(self, width: int, height: int) -> None:
        """ Generate a maze with the given width and height """
        pass

    def get_maze(self):
        """ Return the generated Maze """

    def get_dimensions(self):
        """ Return the dimensions fo the maze """
        return self.width, self.height

    def get_cell(self, x: int, y: int):
        """ Return the cell in these coordenates """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.maze[y][x]
        else:
            raise IndexError("Cell coordinates out of bounds")

    def set_cell(self, x: int, y: int, value):
        """ Set the cell at the given coordinates to value"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.maze[y][x] = value
        else:
            raise IndexError("Cell coordinates out of bounds")

    def open_path(self, x: int, y: int) -> None:
        """ Open a path to a given coordenates (set cell to 0) """
        self.set_cell(x, y, 1)

    def close_path(self, x: int, y: int) -> None:
        """ Close a path to a given coordenates (set cell to 1) """
        self.set_cell(x, y, 1)

    def space_for_pattern(self, pattern, x: int, y: int) -> bool:
        """ Check if is space enough for the pattern in the maze """
        for dy, row in enumerate(pattern):
            for dx, values in enumerate(row):
                if not (0 <= x + dx < self.width and 0 <= y + dy < self.height):
                    return False
                if self.get_cell(x + dx, y + dy) != 1:
                    return False
        return True

    def add_pattern(self, pattern: list[str] | None = None,
                    x: int, y: int) -> set[tuple[int, int]]:
        """ Add pattern at the center of the Maze """
        for dy, row in enumerate(pattern):
            for dx, value in enumerate(row):
                self.set_cell(x + dx, y + dy, value)

