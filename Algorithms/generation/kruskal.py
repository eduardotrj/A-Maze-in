from typing import Any

from Algorithms.generation.maze_generator import MazeGenerator

# Kruskal's Algorithm
# The idea: treat every logical cell as a node in a union-find (disjoint-set)
# structure, and every wall between two adjacent cells as an edge.
# Shuffle the edges, then carve each wall whose two cells aren't already
# connected — that's the classic
# "randomized minimum spanning tree" approach.

Position = tuple[int, int]
Edge = tuple[Position, Position, Position]


class Kruskal(MazeGenerator):
    """Generate a maze using randomized Kruskal's algorithm."""

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
        """Generate a maze with randomized Kruskal's algorithm."""
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

        cells = [
            (x, y)
            for y in range(1, height, 2)
            for x in range(1, width, 2)
            if (x, y) not in self._locked
        ]

        for x, y in cells:
            self.open_path(x, y)
            self.record.append([x, y])

        parent: dict[Position, Position] = {
            cell: cell
            for cell in cells
        }

        def find(cell: Position) -> Position:
            """Return the root of a union-find set."""
            while parent[cell] != cell:
                parent[cell] = parent[parent[cell]]
                cell = parent[cell]
            return cell

        def union(first: Position, second: Position) -> bool:
            """Join two sets and return False if already connected."""
            first_root = find(first)
            second_root = find(second)

            if first_root == second_root:
                return False

            parent[first_root] = second_root
            return True

        edges: list[Edge] = []

        for x, y in cells:
            right = (x + 2, y)
            down = (x, y + 2)

            if right in parent:
                edges.append(
                    ((x + 1, y), (x, y), right)
                )

            if down in parent:
                edges.append(
                    ((x, y + 1), (x, y), down)
                )

        self._random.shuffle(edges)

        for wall, first, second in edges:
            if not union(first, second):
                continue

            wall_x, wall_y = wall
            self.open_path(wall_x, wall_y)
            self.record.append([wall_x, wall_y])

        if not self.perfect:
            self.braid(0.5, "random")
