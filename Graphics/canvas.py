from typing import Any
from abc import ABC, abstractmethod
from mlx import Mlx
from Graphics.image import ImgData
import numpy as np


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
    def draw_image(self, image, x, y) -> None:
        """ Draw a pixel by coordenates and color """
        pass

    @abstractmethod
    def present(self) -> None:
        pass

    @abstractmethod
    def image_to_memory(self) -> None:
        pass

    @abstractmethod
    def create_image(self, width: int, height: int) -> ImgData:
        """ Generate IMG objets to print in MLX """


class MLXCanvas(Canvas):
    """ Class specifically to manage MiniLibX Functions """
    def __init__(self, window, mlx):
        self.window = window
        self.image
        self.mlx = mlx

    def clear(self, window) -> None:
        self.mlx_clear_window(mlx_ptr: int, window) -> int:

    def draw_pixel(self, x, y, color) -> None:
        # Mlx.mlx_pixel_put()
        pass

    def draw_image(self, image_id, x, y) -> None:
        Mlx.mlx_put_image_to_window(
            self.mlx,
            self.window,
            image_id,
            x,
            y
        )

    def present(self) -> None:
        Mlx.mlx_put_image_to_window()

    def image_to_memory(self, array: np.ndarray, image: ImgData) -> None:
        """" Take and multidimensional array of data from a image and save in
        data address of ImgData"""

        buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        buffer[:, :, :] = array[:, :, :]


    def create_image(self, width: int, height: int) -> ImgData:
        """ Generate IMG objets to print in MLX """
        image = ImgData()
        image.id = Mlx.mlx_new_image(self.mlx, width, height)
        image.width, image.height = (width, height)
        image.data, image.bytesPP, image.bytesPL, image.format = Mlx.mlx_get_data_addr(image.id)

        return image
    

#define TILE 32

