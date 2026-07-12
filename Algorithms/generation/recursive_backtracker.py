from functools import cached_property
import numpy as nu
from Algorithms.generation.maze_generator import MazeGenerator

# ** RECURSIVE BACKTRACKER **
# Selet a random cell as starting point.
# Choose random adjacent cell -> Create a passage if is free.
# When is not more adjacent free cell. Return until when is.
# When return to start point -> No more free cells = Done


class Backtracker(MazeGenerator):
    def __init__(self):
        super().__init__()