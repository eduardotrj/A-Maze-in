

class MazeApplication:

    def __init__(self, settings) -> None:

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

    #def create_grid(self):

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

    app = MazeApplication(settings)

    #   app.run()


if __name__ == "__main__":
    main()


