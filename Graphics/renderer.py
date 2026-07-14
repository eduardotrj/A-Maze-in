from abc import ABC, abstractmethod
import numpy as np
#import cv2
import time
from Graphics.theme import ThemeManager

from enum import Enum


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
        #self.theme = 'default'
        self.animated = False
        #self.assets_name = ('wall', 'path', 'bg', 'start', 'exit', 'mark',
        #                    'solve_n', 'solve_ne', 'solve_e', 'solve_es',
        #                    'solve_s', 'solve_sw', 'solve_w', 'solve_wn')
#        self.load_assets()
        self.theme = ThemeManager(self.canvas, self.tile_size)
#        # Load Graphics:\

## ? Better to use a list to avoid print 300 same sht
#    def update_assets(self):
#        self.canvas.detele_images(self.wall)
#        self.canvas.detele_images(self.path)
#        self.canvas.detele_images(self.background)
#        self.canvas.detele_images(self.start)
#        self.canvas.detele_images(self.exit)
#        self.canvas.detele_images(self.mark)
#        self.canvas.detele_images(self.solve_n)
#        self.canvas.detele_images(self.solve_ne)
#        self.canvas.detele_images(self.solve_e)
#        self.canvas.detele_images(self.solve_es)
#        self.canvas.detele_images(self.solve_s)
#        self.canvas.detele_images(self.solve_sw)
#        self.canvas.detele_images(self.solve_w)
#        self.canvas.detele_images(self.solve_wn)
#        self.load_assets()

    #def load_assets(self):
    #    """ Manage and save all assets automatically """

    #    # 1.Get all possible assets themes:

    #    # 2.Load all images using dic{tuple}
    #    self.wall = self.img_array('wall.png')
    #    self.path = self.img_array('path.png')
    #    self.background = self.img_array('bg.png')
    #    self.start = self.img_array('start.png')
    #    self.exit = self.img_array('exit.png')
    #    self.mark = self.img_array('mark.png')
    #    self.solve_n = self.img_array('solve_n.png')
    #    self.solve_ne = self.img_array('solve_ne.png')
    #    self.solve_e = self.img_array('solve_e.png')
    #    self.solve_es = self.img_array('solve_es.png')
    #    self.solve_s = self.img_array('solve_s.png')
    #    self.solve_sw = self.img_array('solve_sw.png')
    #    self.solve_w = self.img_array('solve_w.png')
    #    self.solve_wn = self.img_array('solve_wn.png')

    def new_theme(self, theme) -> None:
        self.theme.set_theme(theme)

    def draw(self, maze) -> None:
        """ Call others Draw() Methods in orden """
        # 1. Background.\
        # 2. Fill area.\
        # 3. Put external Wall
        self.canvas.clear(self.window)
        self.draw_grid(maze)
        # 4. Print inner maze
        self.draw_maze(maze)
        # 5. put enter/exit
        self.draw_pointers(maze)
        # 6. Put markets
        print("Renderer: Drawing maze ")

    def draw_grid(self, maze) -> None:
        """ Draw the grid surrounded by a wall """
        #? Can separate walls from bg for animation.
        max_height = maze.height * 2
        max_width = maze.width * 2

        # Maze not located in 00. require -1 to full frame filling
        for y in range(-1, max_height):
            self.canvas.syncro()
            for x in range(-1, max_width):
                if (y == -1 or y == (max_height - 1)):
                    self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.WALL)    # hexadecimal n
                    )
                elif (x == -1 or x == (max_width - 1)):
                    self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.WALL)     # hexadecimal n
                    )
                else:
                    self.draw_cell(
                        x,
                        y,
                        self.theme.get_image(Tile.PATH)     # hexadecimal n
                    )
        #   self.canvas.clear()
        #   self.canvas.draw_pixel()

    def draw_maze(self, maze) -> None:
        """ Draw the grid with the maze cells """
        for y in range(maze.height):
            for x in range(maze.width):
                #time.sleep(0.1)
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
        #tile = self.tile_size
        x *= 2
        y *= 2
        # Printing in the center
        #screen_x = (x * tile)
        #screen_y = (y * tile)
        self.canvas.syncro()
        if (cell & NORTH):
            self.draw_cell(
                x,
                y-1,
                self.theme.get_image(Tile.WALL)     # hexadecimal n
            )
            self.draw_cell(
                x-1,
                y-1,
                self.theme.get_image(Tile.WALL)     # hexadecimal n
            )
            self.draw_cell(
                x+1,
                y-1,
                self.theme.get_image(Tile.WALL)     # hexadecimal n
            )

        if cell & EAST:
            self.draw_cell(
                x+1,
                y-1,
                self.theme.get_image(Tile.WALL)
            )
            self.draw_cell(
                x+1,
                y,
                self.theme.get_image(Tile.WALL)
            )
            self.draw_cell(
                x+1,
                y+1,
                self.theme.get_image(Tile.WALL)
            )
        if cell & SOUTH:
            self.draw_cell(
                x-1,
                y+1,
                self.theme.get_image(Tile.WALL)
            )
            self.draw_cell(
                x,
                y+1,
                self.theme.get_image(Tile.WALL)
            )
            self.draw_cell(
                x+1,
                y+1,
                self.theme.get_image(Tile.WALL)
            )
        if cell & WEST:
            self.draw_cell(
                x-1,
                y-1,
                self.theme.get_image(Tile.WALL)
            )
            self.draw_cell(
                x-1,
                y,
                self.theme.get_image(Tile.WALL)
            )
            self.draw_cell(
                x-1,
                y+1,
                self.theme.get_image(Tile.WALL)
            )

    #def merge_images(self, bg_data, fg_data, width, height):
    #    """ Takes 2 images as BGRA arrays
    #        Merge and gives another image
    #    """
    #    if bg_data.shape != fg_data.shape:
    #    # Resize foreground to match background if needed
    #        fg_data = cv2.resize(fg_data, (bg_data.shape[1], bg_data.shape[0]))

    #    # Split channels
    #    bg_bgr = bg_data[:, :, :3].astype(np.float32)
    #    bg_a = bg_data[:, :, 3].astype(np.float32) / 255.0

    #    fg_bgr = fg_data[:, :, :3].astype(np.float32)
    #    fg_a = fg_data[:, :, 3].astype(np.float32) / 255.0

    #    # "Over" compositing formula (Porter-Duff)
    #    out_a = fg_a + bg_a * (1 - fg_a)

    #    # Avoid division by zero where out_a == 0
    #    safe_out_a = np.where(out_a == 0, 1, out_a)

    #    out_bgr = (
    #        fg_bgr * fg_a[..., None] +
    #        bg_bgr * bg_a[..., None] * (1 - fg_a[..., None])
    #    ) / safe_out_a[..., None]

    #    out_bgr = np.clip(out_bgr, 0, 255).astype(np.uint8)
    #    out_a = np.clip(out_a * 255, 0, 255).astype(np.uint8)

    #    result = cv2.merge((out_bgr[:, :, 0], out_bgr[:, :, 1], out_bgr[:, :, 2], out_a))
    #    return result


        ## Conver buffers into Numpy matrix (uint8) and reshape it
        #bg_img = np.frombuffer(bg_data, dtype=np.uint8).reshape((height, width, 4))
        #fg_img = np.frombuffer(fg_data, dtype=np.uint8).reshape((height, width, 4))

        ## Sepparate color+alpha channels for front image.
        #fg_rgb = fg_img[:, :, 0:3]
        #fg_alpha = fg_img[:, :, 3] / 255.0  # Normalizar de 0-255 a 0.0-1.0

        ## Sepparate color+alpha channels for background.
        #bg_rgb = bg_img[:, :, 0:3]
        #bg_alpha = bg_img[:, :, 3] / 255.0  # Normalizar de 0-255 a 0.0-1.0

        ## Calculate alpha: alpha_out = alpha_fg + alpha_bg * (1 - alpha_fg)
        #out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)

        ## Avoid zero division for transparent pixels
        #out_alpha_safe = np.where(out_alpha == 0, 1.0, out_alpha)

        ## Expand transparent zones to multiplicate with channels (B, G, R)
        #fg_alpha_factor = fg_alpha[:, :, np.newaxis]
        #bg_alpha_factor = bg_alpha[:, :, np.newaxis]
        #out_alpha_factor = out_alpha_safe[:, :, np.newaxis]

        ## Apply Alpha Blending for color channels: color_out =
        ## (color_fg * α_fg + color_bg * α_bg * (1 - α_fg)) / α_out
        #out_rgb = (fg_rgb * fg_alpha_factor + bg_rgb * bg_alpha_factor
        #           * (1.0 - fg_alpha_factor)) / out_alpha_factor

        ## Reconversion of channels values into 8 bits 
        #out_rgb = np.clip(out_rgb, 0, 255).astype(np.uint8)
        #out_alpha = np.clip(out_alpha * 255, 0, 255).astype(np.uint8)

        ## Rebuild original channels BGRA
        #merged_img = cv2.merge([out_rgb[:, :, 0], out_rgb[:, :, 1],
        #                        out_rgb[:, :, 2], out_alpha])

        ## Regenerate raw bytes data for MiniLibx
        # return merged_img  # .tobytes()

    def draw_pointers(self, maze) -> None:
        self.canvas.syncro()
        self.draw_cell(
            maze.entry[0] * 2 - 2,
            maze.entry[1] * 2 - 2,
            self.theme.get_image(Tile.START)
        )
        self.draw_cell(
            (maze.exit[0] * 2 - 2),
            (maze.exit[1] * 2 - 2),
            self.theme.get_image(Tile.EXIT)
        )

    #def draw_complex(self, x, y, img_base, img_top) -> None:
    #    screen_x = x * self.tile_size + self.tile_size
    #    screen_y = y * self.tile_size + self.tile_size
    #    self.canvas.draw_double_image(
    #        img_base,
    #        img_top,
    #        screen_x,
    #        screen_y
    #    )

    def draw_cell(self, x, y, image) -> None:
        """ Printing a till with """
        screen_x = x * self.tile_size + self.tile_size
        screen_y = y * self.tile_size + self.tile_size

        self.canvas.draw_image(
            image,
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
        pass

    def decoding_data(self):
        pass
        # 4hex = 9 positions (h * 2 = 1)
