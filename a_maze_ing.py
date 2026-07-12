from Graphics.window import MLXWindow
from Graphics.canvas import MLXCanvas
from Graphics.renderer import MazeRenderer
from Maze.generator import Generator
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

        # instance components  #! NOT HERE, Properties of Maze and renderer class.
        # self.something = Something()
        self.width = 640
        self.height = 900
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

    # ! TEMPORALLY UBICATED HERE --> To EvenManager
    def hook_setup(self) -> None:
        #self.ve.mlx_mouse_hook(self.window, on_mouse, None)
        self.ve.mlx_key_hook(self.window.win, self.on_key, None)
        self.ve.mlx_hook(self.window.win, 33, 0, self.on_close, None)

    def on_key(self, keynum: int, _param) -> None:
        if keynum == 65307:
            self.window.close()
            self.window.end()

    def on_close(self, _param) -> None:
        self.window.close()
        self.window.end()

        # ! ----------------------------------------

    #def initialize(self) -> None:
    #    """ Initialize the different classes to generate data """
    #    A = 10
    #    B = 11
    #    C = 12
    #    D = 13
    #    E = 14
    #    F = 15

    #    data = (
    #        (9, 5, 3, B),
    #        (C, 3, C, 2),
    #        (B, E, B, A),
    #        (C, 5, 4, 6),
    #    )

    #    maze = Maze(data, (1, 2), (2, 2), 0000)
    #    self.renderer.draw(maze)

    def initialize(self) -> None:
        """ Initialize the different classes to generate data """

        new_maze: Maze = Generator.generate_maze(20, 20, "recursive_backtraker")
        self.renderer.draw(new_maze)




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

        self.hook_setup()
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
