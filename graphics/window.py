from typing import Any
from abc import ABC, abstractmethod
from mlx import Mlx
from Graphics import eventManager


class IWindow(ABC):
    """ Abstract class to generate Graphic window control classes """

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def loop(self):
        pass

    def register_callback(self, event, callback):
        """ Read for Keyboard inputs """
        pass


class MLXWindow(IWindow):
    """ Manage the window creation and inputs control -> Deals With Mlx """
    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.title = title
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
