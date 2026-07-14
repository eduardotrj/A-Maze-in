from typing import Any
from abc import ABC, abstractmethod
from mlx import Mlx
from Graphics.image import ImgData
import numpy as np
import ctypes

# Use to create default images and edit it.
#from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageMode

#from PIL.Image import Image as PillowImage
#def console_text(self, string: str, font_size: int) -> PillowImage:

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
    def image_to_memory(self, array: np.ndarray, image: ImgData) -> None:
        pass

    @abstractmethod
    def create_image(self, width: int, height: int) -> ImgData:
        """ Generate IMG objets to print in MLX """
        pass


class MLXCanvas(Canvas):
    """ Class specifically to manage MiniLibX Functions """
    def __init__(self, window, visual_engine, mlx, width, height, tile):
        self.window = window
        #self.image
        self.mlx = mlx
        self.ve: Mlx = visual_engine

        self.tile_size = tile
        self.maze_width: int = width
        self.maze_height: int = height
        self.base_width = (self.maze_width * 2 + 1) * self.tile_size
        self.base_height = (self.maze_height * 2 + 1) * self.tile_size

    def syncro(self) -> None:
        """ Improve speed and avoid losing data on the window """
        self.ve.mlx_do_sync(self.window.mlx)

    def clear(self, window) -> None:
        self.ve.mlx_clear_window(self.mlx, self.window.win)

    def draw_pixel(self, x, y, color) -> None:
        # self.ve.mlx_pixel_put()
        pass

    #def draw_image(self, image_data, x, y) -> None:
    def draw_image(self, image, x, y) -> None:
        #mem_img = np.zeros((self.base_height, self.base_width, 4), dtype=np.uint8)
        #image = self.create_image(self.base_width, self.base_height)
        #image_height, image_width = image_data.shape[:2]
        #image = self.create_image(image_width, image_height)
        #mem_img[x:x+self.tile_size, y:y+self.tile_size] = image_data
        #self.image_to_memory(image_data, image)  # mem_img -> image_data
        #self
        self.ve.mlx_put_image_to_window(
            self.mlx,
            self.window.win,
            image.id,
            x,
            y
        )
    #def draw_double_image(self, image_base, image_top, x, y) -> None:
    #    #mem_img = np.zeros((self.base_height, self.base_width, 4), dtype=np.uint8)
    #    #image = self.create_image(self.base_width, self.base_height)
    #    image_height, image_width = image_base.shape[:2]
    #    imageb = self.create_image(image_width, image_height)
    #    image_height, image_width = image_top.shape[:2]
    #    imaget = self.create_image(image_width, image_height)
    #    #mem_img[x:x+self.tile_size, y:y+self.tile_size] = image_data
    #    self.image_to_memory(image_base, imageb)  # mem_img -> image_data
    #    self.image_to_memory(image_top, imaget)
    #    self.ve.mlx_put_image_to_window(
    #        self.mlx,
    #        self.window.win,
    #        imageb.id,
    #        x,
    #        y
    #    )
    #    self.ve.mlx_put_image_to_window(uptate_assets
    #        self.mlx,
    #        self.window.win,
    #        imaget.id,
    #        x,
    #        y
    #    )

    def present(self) -> None:
        # self.ve.mlx_put_image_to_window()
        pass

    def detele_images(self, id_image):
        self.ve.mlx_destroy_image(self.mlx, id_image)

    #def load_image(self, filename):
    #    image_array = self.img_array(filename)
    def load_image(self, file):
        h, w = file.shape[:2]
        image = self.create_image(w, h)
        self.image_to_memory(file, image)

        return image

    def image_to_memory(self, array: np.ndarray, image: ImgData) -> None:
        """" Take and multidimensional array of data from a image and save in
        data address of ImgData"""

        buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        buffer[:, :, :] = array[:, :, :]
        # --------

        # # Obtener el puntero de memoria de tu imagen de MLX
        #img_ptr, bpp, line_length, endian = self.ve.mlx_get_data_addr(mlx_image_obj.id)
        
        ## Convertir la matriz de OpenCV a bytes crudos aquí
        #raw_bytes = cv2_image.tobytes()
        
        ## Copiar los bytes al buffer de MiniLibX
        #img_ptr[0:len(raw_bytes)] = raw_bytes

    # ! Change code to call one time per image only (draw_image);
    def create_image(self, width: int, height: int) -> ImgData:
        """ Generate IMG objets to print in MLX """
        image = ImgData()
        image.id = self.ve.mlx_new_image(self.mlx, width, height)
        image.width, image.height = (width, height)
        image.data, image.bytesPP, image.bytesPL, image.format \
            = self.ve.mlx_get_data_addr(image.id)

        return image
