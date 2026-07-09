from abc import ABC, abstractmethod
import numpy as np
import cv2

# Working process:
# Renderer -> Canvas -> MiniLibx
# Window -> EventManager -> MiniLibx


#   renderer.draw(grid)
class Renderer(ABC):
    """
    Convert data into Graphics

    """

    @abstractmethod
    def draw(self) -> None:
        """ Call others Draw() Methods in orden """
        pass

    @abstractmethod
    def draw_grid(self, maze) -> None:
        """ Draw the grid with the elements """
        pass

    @abstractmethod
    def draw_cell(self, x, y, cell) -> None:
        """ Print each cell """
        pass

    @abstractmethod
    def draw_solution(self, path) -> None:
        pass


class MazeRenderer(Renderer):
    """
    Render a Maze
    """
    def __init__(self, window, canvas, size: int = 32) -> None:
        self.window = window
        self.tile_size = size   # Pixel size
        self.canvas = canvas    # To print into MiniLibx
        self.theme = 'default'
        # Load Graphics:\
        self.wall = self.img_array('wall.png')
        self.path = self.img_array('path.png')
        self.background = self.img_array('bg.png')
        self.start = self.img_array('start.png')
        self.exit = self.img_array('exit.png')
        self.mark = self.img_array('mark.png')
        self.solve_n = self.img_array('solve_n.png')
        self.solve_ne = self.img_array('solve_ne.png')
        self.solve_e = self.img_array('solve_e.png')
        self.solve_es = self.img_array('solve_es.png')
        self.solve_s = self.img_array('solve_s.png')
        self.solve_sw = self.img_array('solve_sw.png')
        self.solve_w = self.img_array('solve_w.png')
        self.solve_wn = self.img_array('solve_wn.png')

    def img_array(self, filename: str, resizing: bool = False) -> np.ndarray:
        """ Transform an img into a data array with BGRA channels """
        # ?Use try catch or any way if not image? OR put DEFAULT?/
        image = cv2.imread(f"Assets/{self.theme}/{filename}")

        if image is None:
            return np.asanyarray(None)
        image_argb = cv2.cvtColor(image, code=cv2.COLOR_BGR2BGRA)

        if resizing is True:
            size = self.tile_size
            resize_img = cv2.resize(image_argb, (size, size))
            return np.asarray(resize_img, dtype=np.uint8)
        return np.asarray(image_argb, dtype=np.uint8)

    def draw(self) -> None:
        """ Call others Draw() Methods in orden """
        print("Renderer: Drawing maze ")

    def draw_grid(self, maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                self.draw_cell(
                    x,
                    y,
                    maze.cell(x, y)     # hexadecimal n
                )
        #   self.canvas.clear()
        #   self.canvas.draw_pixel()

    def draw_cell(self, x, y, cell) -> None:
        NORTH = 0x1
        EAST = 0x2
        SOUTH = 0x4
        WEST = 0x8

        screen_x = x * self.tile_size
        screen_y = y * self.tile_size

        self.canvas.draw_image(
            self.path,
            screen_x,
            screen_y
        )

        if cell & NORTH:
            self.canvas.draw_image(
                #   self.wall_north,
                self.wall,
                screen_x,
                screen_y
            )

        if cell & EAST:
            self.canvas.draw_image(
                #   self.wall_east,
                self.wall,
                screen_x,
                screen_y
            )

        if cell & SOUTH:
            self.canvas.draw_image(
                #   self.wall_south,
                self.wall,
                screen_x,
                screen_y
            )

        if cell & WEST:
            self.canvas.draw_image(
                #   self.wall_west,
                self.wall,
                screen_x,
                screen_y
            )

    def draw_solution(self, path) -> None:
        """ Draw the solution (PATH)"""
        pass

    def generate_background(self) -> None:
        """ Draw Background for the Maze """
        pass

    def generate_walls(self) -> None:
        """ Draw the walls: Originally full all with walls """
        pass

    def generate_floow(self) -> None:
        """ Draw the floor """
        pass

    def generate_points(self) -> None:
        """ Draw start and End point in the maze """
