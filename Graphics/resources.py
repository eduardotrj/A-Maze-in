from enum import Enum, IntFlag


class Tile(str, Enum):
    WALL = "wall.png"
    PATH = "path.png"
    MARK = "mark.png"
    EXIT = "exit.png"
    START = "start.png"
    S_N = "solve_n.png"
    S_NE = "solve_ne.png"
    S_E = "solve_e.png"
    S_ES = "solve_es.png"
    S_S = "solve_s.png"
    S_SW = "solve_sw.png"
    S_W = "solve_w.png"
    S_NW = "solve_nw.png"
    S_EW = "solve_ew.png"
    S_NS = "solve_ns.png"


class HexaWall(IntFlag):
    NORTH = 0x1
    EAST  = 0x2
    SOUTH = 0x4
    WEST  = 0x8


WALL_SEGMENTS = {
    HexaWall.NORTH: [
        (-1, -1),
        ( 0, -1),
        ( 1, -1),
    ],
    HexaWall.EAST: [
        (1, -1),
        (1,  0),
        (1,  1),
    ],
    HexaWall.SOUTH: [
        (-1, 1),
        ( 0, 1),
        ( 1, 1),
    ],
    HexaWall.WEST: [
        (-1, -1),
        (-1,  0),
        (-1,  1),
    ],
}