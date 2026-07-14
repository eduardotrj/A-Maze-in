from Graphics.window import MLXWindow
from Graphics.canvas import MLXCanvas
from Graphics.renderer import MazeRenderer
from Graphics.eventManager import EventManager
from Maze.generator import Generator
from Maze.model import Maze
from mlx import Mlx
import os
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
        self.width = 3
        self.height = 3
        self.grid = None
        self.grid_width = 0
        self.grid_height = 0
        self.generator = None
        self.solver = None
        self.tile_size = 32
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self.theme_index = 0

        # Init Graphics
        self.ve = Mlx()     # VisualEngine
        #self.window
        #self.canvas
        #self.renderer

    def read_confg(self) -> None:

        # Data got it from reading file.
        width_size = 6
        height_size = 6

        self.entry = (1, 1)
        self.exit = (3, 3)

        self.grid_width = width_size
        self.grid_height = height_size

        self.width = 32 * (width_size * 2 + 1)
        self.height = 32 * (height_size * 2 + 1)

        self.window = MLXWindow(self.width, self.height, "A-Maze-Ing", self.ve)
        self.control = EventManager(self.ve, self.window, self)

        self.get_themes()

    # ! TEMPORALLY UBICATED HERE --> To EvenManager
    #def hook_setup(self) -> None:
    #    #self.ve.mlx_mouse_hook(self.window, on_mouse, None)
    #    self.ve.mlx_key_hook(self.window.win, self.on_key, None)
    #    self.ve.mlx_hook(self.window.win, 33, 0, self.on_close, None)

    #def on_key(self, keynum: int, _param) -> None:
    #    if keynum == 65307:
    #        self.window.close()
    #        self.window.end()
    #    elif keynum == 114:

    #def on_close(self, _param) -> None:
    #    self.window.close()
    #    self.window.end()

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

        self.canvas = MLXCanvas(self.window, self.ve, self.window.mlx,
                                self.width, self.height, self.tile_size)
        self.renderer = MazeRenderer(self.window, self.canvas, self.tile_size)

        self.create_maze()

    def create_maze(self) -> None:
        new_maze: Maze = Generator.generate_maze(
            (self.grid_width * 2 + 1),
            (self.grid_height * 2 + 1),
            self.entry,
            self.exit,                                              
            "recursive_backtraker")
        new_maze.print_values()
        self.renderer.draw(new_maze)

    def run(self) -> None:
        """ Execute the functions """

        self.read_confg()
        self.control.hook_setup()
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

    def get_themes(self):
        cwd = os.getcwd()
        # Get filesname
        # filenames = next(os.walk(f"{cwd}/Assets/"), (None, None, []))[2]
        dir_path = cwd + "/Assets/"
        self.themes = [f for f in os.listdir(dir_path) if os.path.isdir(
            os.path.join(dir_path, f))]

    def select_theme(self):
        self.theme_index = (self.theme_index + 1) % len(self.themes)
        print(self.themes[self.theme_index])
        self.renderer.new_theme(self.themes[self.theme_index])
        #   self.renderer.theme = self.themes[self.theme_index]


def main() -> None:
    #   Eray Input
    #   settings = load_settings("settings.json")
    app = MazeApplication()

    app.run()


if __name__ == "__main__":
    main()
