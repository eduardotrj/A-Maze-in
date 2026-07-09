from typing import Any
from abc import ABC, abstractmethod
from mlx import Mlx


class Canvas(ABC):
    """ Abstract class to generate graphic controlers """
    @abstractmethod
    def clear(self, window) -> None:
        pass

    @abstractmethod
    def draw_pixel(self, x, y, color) -> None:
        """ Draw a pixel by coordenates and color """
        pass

    @abstractmethod
    def present(self) -> None:
        pass


class MLXCanvas(Canvas):
    """ Class specifically to manage MiniLibX Functions """
    def __init__(self, window):
        self.window = window
        self.image

    def clear(self, window) -> None:
        Mlx.mlx_clear_window(mlx_ptr: int, window) -> int:

    def draw_pixel(self, x, y, color) -> None:
        # Mlx.mlx_pixel_put()
        pass

    def present(self) -> None:
        Mlx.mlx_put_image_to_window()


#define TILE 32

