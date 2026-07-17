import os
import sys
from pydantic import ValidationError
from mlx import Mlx

from Graphics.window import MLXWindow
from Graphics.canvas import MLXCanvas
from Graphics.renderer import MazeRenderer
from Graphics.eventManager import EventManager
from Maze.generator import Generator
from Maze.model import Maze
from Maze.patterns import PATTERN
from Config import ConfigParser, MazeConfig


# Example import:
# from Folder.file import Class

#   from Graphic.window import Window
#   from Config.loader import ...
#   from Maze.model import
#   from Maze.solver import
#   from Algorithms.Generation.recursive_backtracker import


class MazeApplication:
    """Coordinate all application components."""

    def __init__(self, settings: MazeConfig) -> None:
        self.settings = settings

        self.tile_size = 32
        self.theme_index = 0

        self.grid = None
        self.generator = None
        self.solver = None

        # Configuration values
        self.grid_width = settings.width
        self.grid_height = settings.height

        self.entry = settings.entry
        self.exit = settings.exit_

        self.output_file = settings.output_file
        self.perfect = settings.perfect
        self.seed = settings.seed

        self.algorithm_name = settings.generator or "prim"

        self.animation = (
            settings.animation
            if settings.animation is not None
            else True
        )

        self.speed = settings.speed or 300

        # Window size in pixels
        self.width = self.tile_size * (self.grid_width * 2 + 1)
        self.height = self.tile_size * (self.grid_height * 2 + 1)

        # Visual engine
        self.ve = Mlx()

        # verify the settings
        print(self.settings.model_dump(by_alias=True))

    def read_confg(self) -> None:

        # Data got it from reading file.
        width_size = 10
        height_size = 10

        self.entry = (1, 1)
        self.exit = (9, 9)

        self.grid_width = width_size
        self.grid_height = height_size

        self.width = self.tile_size * (width_size * 2 + 1)
        self.height = self.tile_size * (height_size * 2 + 1)

        self.window = MLXWindow(self.width, self.height, "A-Maze-Ing", self.ve)
        self.control = EventManager(self.ve, self.window, self)

        self.get_themes()

    def initialize_window(self) -> None:
        """Create the graphical window and event manager."""
        self.window = MLXWindow(
            self.width,
            self.height,
            "A-Maze-Ing",
            self.ve,
        )

        self.control = EventManager(
            self.ve,
            self.window,
            self,
        )

        self.get_themes()

    def initialize(self) -> None:
        """ Initialize the different classes to generate data """

        self.canvas = MLXCanvas(self.window, self.ve, self.window.mlx,
                                self.width, self.height, self.tile_size)
        # ! Use full size window to print the screen with everything.
        # Have in mind if add text
        self.renderer = MazeRenderer(self.window, self.canvas, self.tile_size)

        self.create_maze()

    def create_maze(self) -> None:
        """Generate and render a maze."""
        self.maze = Generator.generate_maze(
            width=self.grid_width * 2 + 1,
            height=self.grid_height * 2 + 1,
            entry=self.entry,
            exit=self.exit,
            name=self.algorithm_name,
            # pattern=PATTERN["C42"],
            pattern=PATTERN["P_42"],
            seed=self.seed,
        )

        self.maze.print_values()
        self.renderer.draw(self.maze, self.animation)

    def update_style(self) -> None:
        self.renderer.draw(self.maze, self.animation)

    def run(self) -> None:
        """Run the application."""
        # self.read_confg()
        self.initialize_window()
        self.control.hook_setup()
        self.initialize()
        self.ve.mlx_do_sync(self.window.mlx)
        self.window.loop()

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

    def select_theme(self, next: int):
        self.theme_index = (self.theme_index + next) % len(self.themes)
        if self.theme_index < 0:
            self.theme_index = len(self.themes)
        print(self.themes[self.theme_index])
        self.renderer.new_theme(self.themes[self.theme_index])
        #   self.renderer.theme = self.themes[self.theme_index]

    # ! Manage to fix fake namings
    def change_algorithm(self):
        list = Generator.list_generators()
        new_index = (list.index(self.algorithm_name) + 1) % len(list)
        self.algorithm_name = list[new_index]
        self.create_maze()


def main() -> None:
    #   Eray Input
    #   settings = load_settings("settings.json")
    """Load configuration and run the application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        raw_settings = ConfigParser(sys.argv[1]).parse()
        settings = MazeConfig.model_validate(raw_settings)

    except OSError as err:
        print(f"File error: {err}")
        return

    except ValidationError as err:
        print(f"Config validation error:\n{err}")
        return

    except ValueError as err:
        print(f"Config parser error: {err}")
        return

    app = MazeApplication(settings)
    app.run()


if __name__ == "__main__":
    main()
