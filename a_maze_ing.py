from Graphics.window import IWindow
from Graphics.canvas import MLXCanvas
from Graphics.renderer import MazeRenderer
# Example import:
# from Folder.file import Class

#   from Graphic.window import Window
#   from Config.loader import ...
#   from Maze.model import
#   from Maze.solver import
#   from Algorithms.Generation.recursive_backtracker import


class MazeApplication:
    """ Class coordinate all objs (controller) """

    def __init__(self, settings) -> None:

        self.settings = settings

        # instance components
        # self.something = Something()

        self.grid = None
        self.generator = None
        self.solver = None

        # Init Graphics
        self.window = IWindow()
        self.canvas = MLXCanvas(800, 600)
        self.renderer = MazeRenderer(self.canvas)

    def initialize(self) -> None:
        """ Initialize the different classes to generate data """

        # Create the grid to work
        self.create_grid()

        # Create the maze data
        self.create_generator()

        # Create the solution
        self.create_solver()

        # Create window
        self.create_window()

        self.create_renderer()

    #   def create_grid(self):
    #       self.grid = Grid(
    #           self.settings.width,
    #           self.settings.height
    #       )

    def run(self) -> None:
        """ Execute the functions """

        self.renderer.draw()
        self.canvas.present()

        #   self.initialize()

        #   self.generate_maze()
        #   self.graphic.run()

    def check_settings(self) -> None:
        """ Only for testing """
        print("Test")


def main() -> None:
    #   Eray Input
    #   settings = load_settings("settings.json")
    app = MazeApplication(settings)

    app.run()


if __name__ == "__main__":
    main()
