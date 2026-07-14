from pathlib import Path
import numpy as np
import cv2
import os

# import cv2
#import cv2


#class Theme:
#    """ Manage the different themes (styles) """
#    def __init__(self, mlx, name):
#        base = Path("Assets") / name

#        self.wall = mlx.load_png(str(base / "wall.png"))
#        self.path = mlx.load_png(str(base / "path.png"))
#        self.mark = mlx.load_png(str(base / "mark.png"))
#        self.exit = mlx.load_png(str(base / "exit.png"))
#        self.start = mlx.load_png(str(base / "start.png"))
#        self.solve_n = mlx.load_png(str(base / "solve_n.png"))
#        self.solve_ne = mlx.load_png(str(base / "solve_ne.png"))
#        self.solve_e = mlx.load_png(str(base / "solve_e.png"))
#        self.solve_es = mlx.load_png(str(base / "solve_es.png"))
#        self.solve_s = mlx.load_png(str(base / "solve_s.png"))
#        self.solve_sw = mlx.load_png(str(base / "solve_sw.png"))
#        self.solve_w = mlx.load_png(str(base / "solve_w.png"))
#        self.solve_nw = mlx.load_png(str(base / "solve_nw.png"))
#        self.solve_ew = mlx.load_png(str(base / "solve_ew.png"))
#        self.solve_ns = mlx.load_png(str(base / "solve_ns.png"))


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
        #names = [
        #    "classic",
        #    "dungeon",
        #    "future",
        #    "forest",
        #    "ice",
        #    "lava"
        #]

        for theme in list_themes:
            self.themes[theme] = {}

            for file in self.FILES:
                #self.themes[theme][file] = \
                #    self.renderer.img_array(
                #        f"assets/{theme}/{file}"
                #    )
                #filename = Path("Assets") / theme / file
                #filename = self.img_array(f"Assets/{theme}/{file}")
                img_array = self.img_array(theme, file)
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
            return np.asanyarray(None)
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
