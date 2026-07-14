from functools import cached_property
import numpy as nu
from Algorithms.generation.maze_generator import MazeGenerator

# Kruskal's Algorithm
# The idea: treat every logical cell as a node in a union-find (disjoint-set) structure,
# and every wall between two adjacent cells as an edge. Shuffle the edges, then carve 
# each wall whose two cells aren't already connected — that's the classic 
# "randomized minimum spanning tree" approach.


class Kruskal(MazeGenerator):
    def __init__(self, width: int, height: int, seed: int = None):
        super().__init__(width, height, seed)

    def generate(self, width: int, height: int):
        """ Generate a maze with the given width and height using randomized Kruskal's algorithm """
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]

        # Open every logical cell (odd coordinates)
        cells = [(x, y) for y in range(1, height, 2) for x in range(1, width, 2)]
        for x, y in cells:
            self.maze[y][x] = 0

        # Union-find setup
        parent = {cell: cell for cell in cells}

        def find(cell):
            while parent[cell] != cell:
                cell = parent[cell]
            return cell

        def union(a, b) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False  # already connected -> would create a loop
            parent[ra] = rb
            return True

        # Build the list of candidate walls (edges between adjacent cells)
        edges = []
        for x, y in cells:
            if x + 2 < width:
                edges.append(((x + 1, y), (x, y), (x + 2, y)))       # wall, cell_a, cell_b
            if y + 2 < height:
                edges.append(((x, y + 1), (x, y), (x, y + 2)))

        self._random.shuffle(edges)

        # Carve a wall whenever it connects two disjoint regions
        for (wx, wy), a, b in edges:
            if union(a, b):
                self.maze[wy][wx] = 0