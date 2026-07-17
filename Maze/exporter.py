"""Export a maze to the required output file format."""

from Maze.model import Maze


class MazeExporter:
    """Write maze data to a text file."""

    @staticmethod
    def export(
        maze: Maze,
        solution: str,
        output_file: str,
    ) -> None:
        """Write the maze and its solution to a file."""
        with open(output_file, "w", encoding="utf-8") as file:
            for row in maze.rows:
                hexadecimal_row = "".join(
                    format(cell, "X")
                    for cell in row
                )
                file.write(hexadecimal_row + "\n")

            file.write("\n")

            file.write(
                f"{maze.entry[0]},{maze.entry[1]}\n"
            )
            file.write(
                f"{maze.exit[0]},{maze.exit[1]}\n"
            )
            file.write(solution + "\n")
