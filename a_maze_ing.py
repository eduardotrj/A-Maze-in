from Graphics.window import MLXWindow
from Graphics.canvas import MLXCanvas
from Graphics.renderer import MazeRenderer

from Maze.model import Maze
from mlx import Mlx
# Example import:
# from Folder.file import Class

#   from Graphic.window import Window
#   from Config.loader import ...
#   from Maze.model import
#   from Maze.solver import
#   from Algorithms.Generation.recursive_backtracker import


class MazeApplication:
    """ Class coordinate all objs (controller) """

    def __init__(self) -> None:

        # self.settings = settings

        # instance components
        # self.something = Something()
        self.width = 800
        self.height = 600
        self.grid = None
        self.generator = None
        self.solver = None

        self.tile_size = 32

        # Init Graphics
        self.ve = Mlx()     # VisualEngine
        self.window = MLXWindow(self.width, self.height, "A-Maze-Ing", self.ve)
        self.canvas = MLXCanvas(self.window, self.ve, self.window.mlx,
                                self.width, self.height, self.tile_size)
        self.renderer = MazeRenderer(self.window, self.canvas, self.tile_size)

    # ! TEMPORALLY UBICATED HERE
    def hook_setup(self) -> None:
        #self.ve.mlx_mouse_hook(self.window, on_mouse, None)
        self.ve.mlx_key_hook(self.window, self.on_key, None)
        self.ve.mlx_hook(self.window, 33, 0, self.on_close, None)

    def on_key(self, keynum: int) -> None:
        if keynum == 65307:
            self.window.close()

    def on_close(self) -> None:
        self.window.end()

    def initialize(self) -> None:
        """ Initialize the different classes to generate data """
        A = 10
        B = 11
        C = 12
        D = 13
        E = 14
        F = 15
        data = (
            (9, 3, 9, 5, 5, 1, 5, 5, 3),
            (A, C, 6, 9, 3, A, 9, 3, E),
            (E, 9, 3, A, E, 8, 6, C, 3),
            (9, 6, 8, 6, 9, 4, 5, 7, A),
            (A, F, A, F, A, F, F, F, A),
            (A, F, E, F, 8, 5, 7, F, A),
            (A, F, F, F, A, F, F, F, A),
            (A, 9, 3, F, A, F, D, 5, 2),
            (C, 6, A, F, E, F, F, F, A),
            (B, 9, 6, 9, 3, D, 1, 5, 2),
            (8, 6, 9, 6, C, 5, 6, B, A),
            (A, 9, 6, 9, 1, 7, 9, 4, 6),
            (C, 6, D, 6, C, 5, 4, 5, 7),
        )

        maze = Maze(data, (4, 2), (6, 2), 0000)

        self.renderer.draw_grid(maze)

        # Create the grid to work
        #self.create_grid()

        ## Create the maze data
        #self.create_generator()

        ## Create the solution
        #self.create_solver()

        ## Create window
        #self.create_window()

        #self.create_renderer()

    #   def create_grid(self):
    #       self.grid = Grid(
    #           self.settings.width,
    #           self.settings.height
    #       )

    def run(self) -> None:
        """ Execute the functions """

        self.initialize()
        self.ve.mlx_do_sync(self.window.mlx)
        self.window.loop()

        #self.renderer.draw()
        #self.canvas.present()

        #   self.initialize()d

        #   self.generate_maze()
        #   self.graphic.run()

    def check_settings(self) -> None:
        """ Only for testing """
        print("Test")


def main() -> None:
    #   Eray Input
    #   settings = load_settings("settings.json")
    app = MazeApplication()

    app.run()


if __name__ == "__main__":
    main()
