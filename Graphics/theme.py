from pathlib import Path
import sys
import numpy as np
import random
import cv2
import os


class ThemeManager:

    FILES = [
        "wall.png",
        "path.png",
        "mark.png",
        "exit.png",
        "start.png",
        "solve_n.png",
        "solve_ne.png",
        "solve_e.png",
        "solve_es.png",
        "solve_s.png",
        "solve_sw.png",
        "solve_w.png",
        "solve_nw.png",
        "solve_ew.png",
        "solve_ns.png"
    ]

    WIDTH = 32
    HEIGH = 32

    def __init__(self, canvas, tile_size):
        self.canvas = canvas
        self.themes = {}
        self.current: str = None
        self.tile_size = tile_size
        self.load_all()

    def get_list_themes(self):
        cwd = os.getcwd()
        dir_path = cwd + "/Assets/"
        # Load automatically all themes
        themes = [f for f in os.listdir(dir_path) if os.path.isdir(
            os.path.join(dir_path, f))]
        return themes

    def load_all(self):
        list_themes = self.get_list_themes()

        for theme in list_themes:
            self.themes[theme] = {}

            for file in self.FILES:
                #self.themes[theme][file] = \
                #    self.renderer.img_array(
                #        f"assets/{theme}/{file}"
                #    )
                #filename = Path("Assets") / theme / file
                #filename = self.img_array(f"Assets/{theme}/{file}")

                try:
                    img_array = self.img_array(theme, file)

                except FileNotFoundError:
                    sys.stderr.write(f"{file} Not found. """
                                     "Generating a random image instead")
                    option = int(random.randint(0, 2))

                    if option == 2:
                        img_array = self.generate_brushed_texture()
                    elif option == 1:
                        img_array = self.generate_cellular_texture()
                    else:
                        img_array = self.generate_plane_color()

                img = self.canvas.load_image(img_array)

                # Load images in the memory only onces from here
                self.themes[theme][file] = img

        self.current = self.themes["pokemon"]

    def img_array(self, theme: str, filename: str, resizing: bool = False
                  ) -> np.ndarray:
        """ Transform an img into a data array with BGRA channels """
        # ?Use try catch or any way if not image? OR put DEFAULT?/
        image = cv2.imread(f"Assets/{theme}/{filename}")

        if image is None:
            raise FileNotFoundError(f"Assets/{theme}/{filename}")
            # return np.asanyarray(None)
        image_argb = cv2.cvtColor(image, code=cv2.COLOR_BGR2BGRA)

        if resizing is True:
            size = self.tile_size
            resize_img = cv2.resize(image_argb, (size, size))
            return np.asarray(resize_img, dtype=np.uint8)
        return np.asarray(image_argb, dtype=np.uint8)

    def set_theme(self, name) -> None:
        self.current = self.themes[name]

    def get_image(self, name):
        return self.current[name]

    def generate_plane_color(self):
        """
            Generate random color 32x32 images.
        """
        image = np.zeros((self.HEIGH, self.WIDTH, 3), dtype=np.uint8)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)

        image[:, :, 0] = b
        image[:, :, 1] = g
        image[:, :, 2] = r

        #cv2.imshow(name, image)
        #cv2.imwrite(name, image)
        image_argb = cv2.cvtColor(image, code=cv2.COLOR_BGR2BGRA)
        return np.asarray(image_argb, dtype=np.uint8)

    def generate_cellular_texture(self, num_points=100):
        image = np.zeros((self.HEIGH, self.WIDTH), dtype=np.uint8)
        points = np.column_stack((
            np.random.randint(0, self.WIDTH, num_points),
            np.random.randint(0, self.HEIGH, num_points)
        ))

        # Calculate distance from every pixel to the nearest point
        for y in range(self.HEIGH):
            for x in range( self.WIDTH):
                # Calculate Euclidean distances to all point
                distances = np.linalg.norm(points - np.array([x, y]), axis=1)
                # Distante from closest point
                min_dist = np.min(distances)

                # Map distance to a 0-2555 grayscale range
                val = min(int(min_dist * 5), 255)
                image[y, x] = val

        # Apply a colormap to make it colored
        color_texture = cv2.applyColorMap(image, cv2.COLORMAP_JET)

        image_argb = cv2.cvtColor(color_texture, code=cv2.COLOR_BGR2BGRA)
        return np.asarray(image_argb, dtype=np.uint8)

    def generate_brushed_texture(self):
        # Generate fine white noise:
        noise = np.random.randint(100, 180, (self.HEIGH, self.WIDTH), dtype=np.uint8)

        # Apply horizontal motion blur kernel filter:
        kernel_size = 30
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
        kernel /= kernel_size

        brushed = cv2.filter2D(noise, -1, kernel)

        brushed = cv2.normalize(brushed, None, 0, 255, cv2.NORM_MINMAX)
        image_argb = cv2.cvtColor(brushed, code=cv2.COLOR_BGR2BGRA)
        return np.asarray(image_argb, dtype=np.uint8)
