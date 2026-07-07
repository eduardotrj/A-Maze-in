from typing import Any
from mlx import Mlx


class Window:
    """ Manage the window creation and inputs control -> Deals With Mlx """
    def __init__(self, width: int, height: int, title: str) -> None:
        self.mlx = Mlx.mlx_init()

        self.win = Mlx.mlx_new_window(
            self.mlx,
            width,
            height,
            title
        )

    def register_events(self) -> None:
        """ Read for Keyboard inputs """
        pass

    def loop(self) -> None:
        """ Initiate Graphics """
        Mlx.mlx_loop(self.mlx)

    def close(self) -> None:
        """ Stop Graphics """
        Mlx.mlx_destroy_window(self.mlx, self.win)
