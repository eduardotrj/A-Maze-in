from typing import Any
from .maze_generator import MazeGenerator


class HuntAndKill(MazeGenerator):
    """ Works like Recursvie backtracker without recursive """
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
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.record = []
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        self.lock_pattern(pattern, entry, exit)

        cx: int = entry[0]
        cy: int = entry[1]

        self.maze[cy][cx] = 0
        self.record.append([cx, cy])

        self.valid = True

        while self.valid:
            self._walk(cx, cy)
            cx, cy = self._hunt()

        if not self.perfect:
            self.braid(0.2, "random")

    def _walk(self, cx: int, cy: int) -> None:
        """ Random-walk carving passages until stuck at a dead end """
        while True:
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            self._random.shuffle(directions)
            moved = False

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                wx, wy = cx + dx // 2, cy + dy // 2

                if (0 <= nx < self.width and 0 <= ny < self.height
                        and self.maze[ny][nx] == 1
                        and (nx, ny) not in self._locked
                        and (wx, wy) not in self._locked):
                    self.maze[wy][wx] = 0
                    self.record.append([wx, wy])
                    self.maze[ny][nx] = 0
                    self.record.append([nx, ny])
                    cx, cy = nx, ny
                    moved = True
                    break

            if not moved:
                return  # dead end reached, hand control back to the hunt phase

    def _hunt(self) -> tuple[int, int]:
        """ Scan for the first unvisited cell touching a visited one;
            connect and jump there *Instead recursive is used """
        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                if self.maze[y][x] != 1 or (x, y) in self._locked:
                    continue

                neighbors = []
                for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                    nx, ny = x + dx, y + dy
                    wx, wy = x + dx // 2, y + dy // 2
                    if (0 <= nx < self.width and 0 <= ny < self.height
                            and self.maze[ny][nx] == 0
                            and (nx, ny) not in self._locked
                            and (wx, wy) not in self._locked):
                        neighbors.append((wx, wy))

                if neighbors:
                    wx, wy = self._random.choice(neighbors)
                    self.maze[wy][wx] = 0
                    self.record.append([wx, wy])
                    self.maze[y][x] = 0
                    self.record.append([x, y])
                    return x, y

        self.valid = False  # every cell visited, generation is done
        return 1, 1
