
import sys

from config import ConfigParser, validate_config
from pydantic import ValidationError
# now we have pydantic so this is not used
# from config.validator import ConfigValidator


class MazeApplication:

    def __init__(self, settings: dict[str, object]) -> None:

        self.settings = settings

        self.grid = None
        self.generator = None
        self.solver = None

        self.window = None
        self.renderer = None

    def initialize(self) -> None:

        # Create the grid to work
        self.create_grid()

        # Create the maze data
        self.create_generator()

        # Create the solution
        self.create_solver()

        # Create window
        self.create_window()

        self.create_renderer()

    # def create_grid(self):

    #    self.grid = Grid(
    #        self.settings.width,
    #        self.settings.height
    #    )

    def run(self) -> None:

        self.initialize()

        #   self.generate_maze()


def main() -> None:

    #   Eray Input
    #   settings = load_settings("settings.json")

    """Run the A-Maze-ing program."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        raw_settings = ConfigParser(sys.argv[1]).parse()
        # now we have pydantic so this is not used
        # settings = ConfigValidator(raw_settings).validate()
        settings = validate_config(raw_settings)
    except OSError as err:
        print(f"File error: {err}")
        return
    except ValidationError as err:
        print(f"Config error:\n{err}")
        return
    except ValueError as err:
        print(f"Config error: {err}")
        return

    print("Config is valid.")
    # print(config)

    app = MazeApplication(settings)
    print(settings)

    #   app.run()


if __name__ == "__main__":
    main()
