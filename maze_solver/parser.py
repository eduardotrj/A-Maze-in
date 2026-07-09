def parse_maze(lines: list[str]) -> list[list[int]]:
    """Convert hexadecimal maze rows into integer cells."""
    maze: list[list[int]] = []

    for line in lines:
        row: list[int] = []

        for char in line.strip():
            row.append(int(char, 16))

        maze.append(row)

    return maze
