from typing import Any
from abc import ABC, abstractmethod
from mlx import Mlx  # type: ignore[import-untyped]
from Graphics.image import ImgData
import numpy as np
# import ctypes

# Use to create default images and edit it.
# from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageMode

# from PIL.Image import Image as PillowImage
# def console_text(self, string: str, font_size: int) -> PillowImage:

#        """Text to image method. Draw with PIL a text as a new image.

#        Args:
#            string (str): The string to write
#            font_size (int): The size of the font
#        Returns:
#            PillowImage: Newly created PIL image of a text
#        """

#        image = Image.new('RGBA', (700, 300), (0, 0, 0, 200))
#        draw = ImageDraw.Draw(image)
#        font = ImageFont.truetype(f'{self.theme}/font.ttf', font_size)
#        draw.text((150, 120), string, font=font)

#        return image


class Canvas(ABC):
    """ Abstract class to generate graphic controlers """
    @abstractmethod
    def clear(self, window: Any) -> None:
        pass

    @abstractmethod
    def draw_pixel(self, x: Any, y: Any, color: Any) -> None:
        """ Draw a pixel by coordenates and color """
        pass

    @abstractmethod
    def draw_image(self, image: Any, x: Any, y: Any) -> None:
        """ Draw a pixel by coordenates and color """
        pass

    @abstractmethod
    def present(self) -> None:
        pass

    @abstractmethod
    def image_to_memory(self, array: np.ndarray, image: ImgData) -> None:
        pass

    @abstractmethod
    def create_image(self, width: int, height: int) -> ImgData:
        """ Generate IMG objets to print in MLX """
        pass


class MLXCanvas(Canvas):
    """ Class specifically to manage MiniLibX Functions """
    def __init__(self, window: Any, visual_engine: Any,
                 mlx: Any, width: Any, height: Any,
                 tile: Any):
        self.window = window
        # self.image
        self.mlx = mlx
        self.ve: Mlx = visual_engine

        self.tile_size = tile
        self.maze_width: int = width
        self.maze_height: int = height
        self.base_width = (self.maze_width * 2 + 1) * self.tile_size
        self.base_height = (self.maze_height * 2 + 1) * self.tile_size

        # 1. Create a single full-screen MLX image container
        self.screen_img = self.ve.mlx_new_image(self.mlx,
                                                self.maze_width,
                                                self.maze_height)

        # 2. Get the memory address data from MLX
        # mlx_get_data_addr returns: (memoryview, bits_per_pixel,
        #                             size_line, endian)
        all_data = self.ve.mlx_get_data_addr(self.screen_img)
        mem_view, bpp, size_line, _ = all_data

        # 3. Wrap the MLX memoryview into a persistent full-screen NumPy array.
        # This writes directly to MLX memory without making slow copies.
        bytes_per_pixel = bpp // 8
        self.screen_array = np.frombuffer(mem_view, dtype=np.uint8).reshape(
            (height, size_line // bytes_per_pixel, bytes_per_pixel)
        )

        # Trim padding if size_line is wider than screen width
        self.screen_array = self.screen_array[:, :self.maze_width, :]

    def syncro(self) -> None:
        """ Improve speed and avoid losing data on the window """
        self.ve.mlx_do_sync(self.window.mlx)

    def clear(self, window: Any) -> None:
        self.ve.mlx_clear_window(self.mlx, self.window.win)

    def draw_pixel(self, x: Any, y: Any, color: Any) -> None:
        # self.ve.mlx_pixel_put()
        pass

    # def draw_image(self, image_data, x, y) -> None:
    def draw_image(self, image: Any, x: Any, y: Any) -> None:
        # mem_img = np.zeros((self.base_height, self.base_width, 4),
        #                    dtype=np.uint8)
        # image = self.create_image(self.base_width, self.base_height)
        # image_height, image_width = image_data.shape[:2]
        # image = self.create_image(image_width, image_height)
        # mem_img[x:x+self.tile_size, y:y+self.tile_size] = image_data
        # self.image_to_memory(image_data, image)  # mem_img -> image_data
        # self
        self.ve.mlx_put_image_to_window(
            self.mlx,
            self.window.win,
            image.id,
            x,
            y
        )

    def clean_buffer(self) -> None:
        self.screen_array.fill(0)

    def copy_to_buffer(self, y_start: Any, y_end: Any,
                       x_start: Any, x_end: Any,
                       image: Any) -> None:
        self.screen_array[y_start:y_end, x_start:x_end] = image

    def print_screen(self, x: Any, y: Any) -> None:
        self.ve.mlx_put_image_to_window(
            self.mlx, self.window.win, self.screen_img, x, y
        )

    def present(self) -> None:
        # self.ve.mlx_put_image_to_window()
        pass

    def detele_images(self, id_image: Any) -> None:
        self.ve.mlx_destroy_image(self.mlx, id_image)

    # def load_image(self, filename):
    #    image_array = self.img_array(filename)
    def load_image(self, file: Any) -> ImgData:
        # Ensure 'file' is actually a NumPy array
        # if not isinstance(file, np.ndarray):
        #    raise TypeError(f"Expected a numpy.ndarray, but got {type(file)}")

        # Ensure the array has at least 2 dimensions (Height, Width)
        # if len(file.shape) < 2:
        #    raise ValueError(f"Expected at least a 2D array,
        #                        but got shape {file.shape}")

        h, w = file.shape[:2]
        image = self.create_image(w, h)
        self.image_to_memory(file, image)

        return image

    def image_to_memory(self, array: np.ndarray, image: ImgData) -> None:
        """" Take and multidimensional array of data from a image and save in
        data address of ImgData"""
        # Input must be always 4 bytes pixel (BGRA/RGBA) -> cv2.COLOR_BGR2BGRA
        buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        buffer[:, :, :] = array[:, :, :]
        # --------

        # # Obtener el puntero de memoria de tu imagen de MLX
        # img_ptr, bpp, line_length, endian =
        # self.ve.mlx_get_data_addr(mlx_image_obj.id)

        # Convertir la matriz de OpenCV a bytes crudos aquí
        # raw_bytes = cv2_image.tobytes()

        # Copiar los bytes al buffer de MiniLibX
        # img_ptr[0:len(raw_bytes)] = raw_bytes

    # ! Change code to call one time per image only (draw_image);
    def create_image(self, width: int, height: int) -> ImgData:
        """ Generate IMG objets to print in MLX """
        image = ImgData()
        image.id = self.ve.mlx_new_image(self.mlx, width, height)
        image.width, image.height = (width, height)
        image.data, image.bytesPP, image.bytesPL, image.format \
            = self.ve.mlx_get_data_addr(image.id)

        return image
