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
        #    self.ve.mlx_clear_window(self.mlx, self.window) -> int:
        pass

    def draw_pixel(self, x, y, color) -> None:
        # self.ve.mlx_pixel_put()
        pass

    def draw_image(self, image_data, x, y) -> None:
        #mem_img = np.zeros((self.base_height, self.base_width, 4), dtype=np.uint8)
        #image = self.create_image(self.base_width, self.base_height)
        # ! Should not create images each time.
        image_height, image_width = image_data.shape[:2]
        image = self.create_image(image_width, image_height)
        #mem_img[x:x+self.tile_size, y:y+self.tile_size] = image_data
        self.image_to_memory(image_data, image)  # mem_img -> image_data
        self
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
    #    self.ve.mlx_put_image_to_window(
    #        self.mlx,
    #        self.window.win,
    #        imaget.id,
    #        x,
    #        y
    #    )

    def present(self) -> None:
        # self.ve.mlx_put_image_to_window()
        pass

    def image_to_memory(self, array: np.ndarray, image: ImgData) -> None:
        """" Take and multidimensional array of data from a image and save in
        data address of ImgData"""


        # 1. Asegurar que los datos de la matriz OpenCV estén guardados de forma contigua en memoria
        # y extraer sus bytes crudos
        raw_bytes = np.ascontiguousarray(array, dtype=np.uint8).tobytes()
        
        # 2. Calcular el tamaño en bytes que requiere almacenar la imagen en MLX
        # (Suele ser alto * bytes por linea de escaneo)
        total_bytes = min(len(raw_bytes), image.height * image.bytesPL)
        
        # 3. Copiar la memoria de Python directamente al puntero de C de MiniLibX
        # ctypes.memmove gestiona de forma automática si image.data es un entero, 
        # un puntero o un buffer compatible, copiando los bytes instantáneamente.
        ctypes.memmove(image.data, raw_bytes, total_bytes)



        #_________________________
        # Calculate total buffer size of image.
        total_bytes = image.height * image.bytesPL

        # Allow Numpy memory rewriting: image.data -> mutable array Python
        data_ptr = ctypes.cast(image.data, ctypes.POINTER(ctypes.c_ubyte))
        buffer_flat = np.ctypeslib.as_array(data_ptr, shape=(total_bytes,))
        
        # Reshape buffer with image size. Safe for memmory align width.
        width_in_pixels = image.bytesPL // 4
        buffer_3d = buffer_flat.reshape((image.height, width_in_pixels, 4))
        
        # Add data (array opencv) to the real MiniLibx buffer
        h, w, c = array.shape
        buffer_3d[:h, :w, :c] = array


        # This option work correctly but doens't allow print transparencies.
        #buffer = np.frombuffer(image.data, dtype=np.uint8).reshape(array.shape)
        #buffer[:, :, :] = array[:, :, :]
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
        image.data, image.bytesPP, image.bytesPL, image.format = self.ve.mlx_get_data_addr(image.id)

        return image
