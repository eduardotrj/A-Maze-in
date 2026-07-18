from typing import Any
from abc import ABC, abstractmethod
from mlx import Mlx  # type: ignore[import-untyped]
#   from Graphics import eventManager


class IWindow(ABC):
    """ Abstract class to generate Graphic window control classes """

    # @abstractmethod
    # def open(self):
    #    pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def loop(self) -> None:
        pass

    @abstractmethod
    def end(self) -> None:
        pass

    # def register_callback(self, event, callback):
    #     """ Read for Keyboard inputs """
    #     pass


class MLXWindow(IWindow):
    """ Manage the window creation and inputs control -> Deals With Mlx """
    def __init__(self, width: int, height: int,
                 title: str, engine: Any) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.ve: Mlx = engine
        self.mlx = self.ve.mlx_init()   # Window

        self.win = self.ve.mlx_new_window(
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
        self.ve.mlx_loop(self.mlx)

    def end(self) -> None:
        """ Initiate Graphics """
        self.ve.mlx_loop_exit(self.mlx)

    def close(self) -> None:
        """ Stop Graphics """
        self.ve.mlx_destroy_window(self.mlx, self.win)
