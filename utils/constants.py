NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = NORTH | EAST | SOUTH | WEST

DIRECTIONS = {
    "N": (0, -1, NORTH),
    "E": (1, 0, EAST),
    "S": (0, 1, SOUTH),
    "W": (-1, 0, WEST),
}

OPPOSITE_WALL = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}
