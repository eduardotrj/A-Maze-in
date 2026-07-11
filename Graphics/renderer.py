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
    def draw(self, obj) -> None:
        """ Call others Draw() Methods in orden """
        pass

    @abstractmethod
    def draw_grid(self, maze) -> None:
        """ Draw the grid with the elements """
        pass

    @abstractmethod
    def draw_cell(self, x, y, img_tile) -> None:
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

    def draw(self, maze) -> None:
        """ Call others Draw() Methods in orden """
        # 1. Background.\
        # 2. Fill area.\
        # 3. Put external Wall
        self.draw_grid(maze)
        # 4. Print inner maze
        self.draw_maze(maze)
        # 5. put markets
        # 6. Put enter/exit
        print("Renderer: Drawing maze ")

    def draw_grid(self, maze) -> None:
        """ Draw the grid surrounded by a wall """
        #? Can separate walls from bg for animation.
        max_height = maze.height * 2
        max_width = maze.width * 2

        # Maze not located in 00. require -1 to full frame filling
        for y in range(-1, max_height):
            for x in range(-1, max_width):
                if (y == -1 or y == (max_height - 1)):
                    print(x, y)
                    self.draw_cell(
                        x,
                        y,
                        self.wall    # hexadecimal n
                    )
                elif (x == -1 or x == (max_width - 1)):
                    self.draw_cell(
                        x,
                        y,
                        self.wall     # hexadecimal n
                    )
                else:
                    self.draw_cell(
                        x,
                        y,
                        self.path     # hexadecimal n
                    )
        #   self.canvas.clear()
        #   self.canvas.draw_pixel()

    def draw_maze(self, maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                self.draw_walls(
                    x,
                    y,
                    maze.cell(x, y)     # hexadecimal n
                )
        #   self.canvas.clear()
        #   self.canvas.draw_pixel()

    def draw_walls(self, x, y, cell) -> None:
        """ Logic to draw the different walls in the maze"""
        NORTH = 0x1
        EAST = 0x2
        SOUTH = 0x4
        WEST = 0x8
        tile = self.tile_size
        x *= 2
        y *= 2
        # Printing in the center
        #screen_x = (x * tile)
        #screen_y = (y * tile)

        if (cell & NORTH):
            self.draw_cell(
                x,
                y-1,
                self.mark     # hexadecimal n
            )
            self.draw_cell(
                x-1,
                y-1,
                self.mark     # hexadecimal n
            )
            self.draw_cell(
                x+1,
                y-1,
                self.mark     # hexadecimal n
            )

        if cell & EAST:
            self.draw_cell(
                x+1,
                y-1,
                self.mark
            )
            self.draw_cell(
                x+1,
                y,
                self.mark
            )
            self.draw_cell(
                x+1,
                y+1,
                self.mark
            )
        if cell & SOUTH:
            self.draw_cell(
                x-1,
                y+1,
                self.mark
            )
            self.draw_cell(
                x,
                y+1,
                self.mark
            )
            self.draw_cell(
                x+1,
                y+1,
                self.mark
            )
        if cell & WEST:
            self.draw_cell(
                x-1,
                y-1,
                self.mark
            )
            self.draw_cell(
                x-1,
                y,
                self.mark
            )
            self.draw_cell(
                x-1,
                y+1,
                self.mark
            )

    def draw_cell(self, x, y, img_tile) -> None:
        """ Printing a till with """
        screen_x = x * self.tile_size + self.tile_size
        screen_y = y * self.tile_size + self.tile_size

        self.canvas.draw_image(
            img_tile,
            screen_x,
            screen_y
        )

    def draw_solution(self, path) -> None:
        """ Draw the solution (PATH)"""
        pass

    def generate_background(self) -> None:
        """ Draw Background for the Maze """
        pass

    #def generate_walls(self, maze) -> None:
    #    """ Draw the walls: Tu surround the area"""
    #    for y in range(0, maze.height):
    #        for x in range(0, maze.width):
    #            if (y == 0 or y == maze.height):


    #    screen_x = x * self.tile_size + self.tile_size
    #    screen_y = y * self.tile_size + self.tile_size

    #    self.canvas.draw_image(
    #        self.path,
    #        screen_x,
    #        screen_y
    #    )


    def generate_floow(self) -> None:
        """ Draw the floor """
        pass

    def generate_points(self) -> None:
        """ Draw start and End point in the maze """

    def decoding_data(self):


        # 4hex = 9 positions (h * 2 = 1)

        n
