import os
import sys
import random
from pydantic import ValidationError
from mlx import Mlx  # type: ignore[import-untyped]
from Graphics.window import MLXWindow
from Graphics.canvas import MLXCanvas
from Graphics.renderer import MazeRenderer
from Graphics.eventManager import EventManager
from Graphics.console import PrintTerminal as prt
from Graphics.logo import LOGO
from Config import ConfigParser, MazeConfig, GeneratorName
from mazegen import Generator, PATTERN, MazeSolver, MazeExporter


class MazeApplication:
    """Coordinate all application components."""

    def __init__(self, settings: MazeConfig) -> None:
        self.settings = settings
        self.logo = LOGO

        self.tile_size = settings.tile_size
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
        self.is_pattern: tuple[tuple[str, ...], ...] | None = (
            PATTERN[settings.is_pattern]
            if (settings.is_pattern is not None
                and settings.is_pattern in PATTERN)
            else None
        )

        self.algorithm_name: GeneratorName = settings.generator or "prim"

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

        # maze solver
        self.solver_name = "bfs"
        self.solution: str | None = None
        self.solution_visible = False

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
        self.renderer = MazeRenderer(self.window, self.canvas, self.tile_size)

        self.create_maze()

    def create_maze(self) -> None:
        """Generate, solve and display a new maze."""
        self.maze = Generator.generate_maze(
            width=self.grid_width * 2 + 1,
            height=self.grid_height * 2 + 1,
            entry=self.entry,
            exit=self.exit,
            name=self.algorithm_name,
            pattern=self.is_pattern,
            seed=self.seed,
            perfect=self.perfect
        )

        self.solution = MazeSolver.solve(
            self.maze,
            self.solver_name,
        )

        if self.solution is None:
            print("Error: no valid path was found")
            return

        try:
            MazeExporter.export(
                maze=self.maze,
                solution=self.solution,
                output_file=self.output_file,
            )
        except OSError as error:
            print(f"Output file error: {error}")
            return

        self.renderer.draw(
            self.maze,
            animation=self.animation,
        )

        if (
            self.solution_visible
            and self.solution is not None
        ):
            self.renderer.draw_solution(
                self.maze,
                self.solution,
            )
        self.print_maze_data()

    def print_maze_data(self) -> None:

        prt.clean_terminal()
        prt.print_title(self.logo)
        prt.print_controls()
        prt.print_separator()
        prt.print_maze_data(self.maze,
                            self.themes[self.theme_index],
                            self.solver_name,
                            self.settings.is_pattern)

    def update_style(self) -> None:
        """Redraw the maze after a visual update."""
        self.renderer.draw(self.maze, self.animation)
        if self.solution_visible:
            self.redraw()

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

    def get_themes(self) -> None:
        cwd = os.getcwd()
        # Get filesname
        # filenames = next(os.walk(f"{cwd}/Assets/"), (None, None, []))[2]
        dir_path = cwd + "/Assets/"
        self.themes = [f for f in os.listdir(dir_path) if os.path.isdir(
            os.path.join(dir_path, f))]

    def select_theme(self, next: int) -> None:
        self.theme_index = (self.theme_index + next) % len(self.themes)
        if self.theme_index < 0:
            self.theme_index = len(self.themes)
        self.renderer.new_theme(self.themes[self.theme_index])
        self.print_maze_data()

    # ! Manage to fix fake namings
    def change_algorithm(self) -> None:
        """Select the next generation algorithm."""
        # generators: list[GeneratorName] = Generator.list_generators()
        generators = Generator.list_generators()
        new_index = (
            generators.index(self.algorithm_name) + 1
        ) % len(generators)

        self.algorithm_name = generators[new_index]
        self.create_maze()

    def random_exit(self) -> None:
        self.exit = (
            random.randint(0, self.grid_width - 1),
            random.randint(0, self.grid_height - 1))

    def redraw(self) -> None:
        """Redraw the current maze without replaying generation."""

        if not self.animation:
            self.renderer.draw(
                self.maze,
                animation=False,
            )
        if (
            self.solution_visible
            and self.solution is not None
        ):
            # self.renderer.load_full_screen(self.maze)
            self.renderer.draw_solution(
                self.maze,
                self.solution,
            )
            self.renderer.draw_marks(self.maze)
        else:
            # Disable animation to hidde path smoothly.
            self.renderer.load_full_screen(self.maze)
            self.renderer.draw_marks(self.maze)

        self.print_maze_data()

    def toggle_solution(self) -> None:
        """Show or hide the existing solution."""
        self.solution_visible = not self.solution_visible
        self.redraw()

    def change_solver(self) -> None:
        """Select the next solving algorithm."""
        solvers = MazeSolver.list_solvers()

        current_index = solvers.index(
            self.solver_name
        )
        next_index = (
            current_index + 1
        ) % len(solvers)

        self.solver_name = solvers[next_index]

        self.solution = MazeSolver.solve(
            self.maze,
            self.solver_name,
        )
        self.redraw()


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
