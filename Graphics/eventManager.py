from typing import Any


class EventManager():
    def __init__(self, visual_engine: Any, window: Any, owner: Any) -> None:
        self.ve = visual_engine
        self.window = window
        self.owner = owner

    def hook_setup(self) -> None:
        # self.ve.mlx_mouse_hook(self.window, self.on_mouse, None)
        self.ve.mlx_key_hook(self.window.win, self.on_key, None)
        self.ve.mlx_hook(self.window.win, 33, 0, self.on_close, None)

    def on_key(self, keynum: int, _param: Any) -> None:
        # Esc -> Exit
        if keynum == 65307:
            self.window.close()
            self.window.end()

        # R -> Remake
        elif keynum == 114 or keynum == 82:
            self.owner.solution_visible = False  # Disable for new Maze
            self.owner.create_maze()

            # A -> Choose algorithm for maze
        elif keynum == 97 or keynum == 65:
            self.owner.change_algorithm()

            # S -> Style Back
        elif keynum == 115 or keynum == 82:
            # self.owner.solution_visible = False
            self.owner.select_theme(-1)
            self.owner.update_style()

            # D -> Style Next
        elif keynum == 100 or keynum == 68:
            # self.owner.solution_visible = False
            self.owner.select_theme(1)
            self.owner.update_style()

            # F -> Change fixing algorithm
        elif keynum == 102 or keynum == 70:
            self.owner.change_solver()

            # W -> Show solution Way/ off
        elif keynum == 119 or keynum == 87:
            self.owner.toggle_solution()

        # E -> Change solver algorithm solution
        elif keynum == 101 or keynum == 69:
            self.owner.change_solver()
# SPEED/ANIMATION ---------------------------
        # ↑ -> Remove Animation
        elif keynum == 65362:
            self.owner.animation = False if self.owner.animation else True
            self.owner.update_style()
        # → -> Increase Speed
        elif keynum == 65363:
            pass
        # ← -> Decrease Speed
        elif keynum == 65361:
            pass
            # ↓ -> Rseset Speed
        elif keynum == 65364 or keynum == 82:
            pass

        # Change patterns -> No : (

    def on_close(self, _param: Any) -> None:
        self.window.close()
        self.window.end()

    # * Adapt to use mouse on screen.
    # def on_mouse(self, button: int, x: int, y: int, params: Any) -> None:
    #    nonlocal path, scale, win, color_i, path_visible
    #    if x < scale * maze.width:  # Check if inside sidebar.
    #        return

    #    if y < 127:  # Regenerate button.
    #        maze.generate()
    #        path = solve_maze(maze)
    #        scale = get_scale()
    #        m.mlx_destroy_window(p, win)
    #        win = create_window(scale * maze.width,
    #                            max(scale * maze.height, 512))
    #        hook_setup()
    #        color_i = (color_i + 1) % len(colors)
    #        render_maze_cells()
    #        if path_visible:
    #            render_path()

    #    elif 127 < y < 255:  # Color button.
    #        color_i = (color_i + 1) % len(colors)
    #        render_maze_cells()
    #        if path_visible:
    #            render_path()

    #    elif 255 < y < 384:  # Path button.
    #        if path_visible:
    #            render_maze_cells()
    #            path_visible = False
    #        else:
    #            render_path()
    #            path_visible = True

    #    elif 384 < y < 512:  # Exit button.
    #        m.mlx_loop_exit(p)
