"""Manage graphical themes and generate fallback textures."""

import os
import random
from typing import Any
import cv2
import numpy as np
import numpy.typing as npt


ImageArray = npt.NDArray[np.uint8]
LoadedTheme = dict[str, Any]
RawTheme = dict[str, ImageArray]


class ThemeManager:
    """Load, store, select, and generate graphical themes."""

    FILES: list[str] = [
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
        "solve_ns.png",
    ]

    COLORMAPS: list[int] = [
        cv2.COLORMAP_JET,
        cv2.COLORMAP_AUTUMN,
        cv2.COLORMAP_OCEAN,
        cv2.COLORMAP_RAINBOW,
        cv2.COLORMAP_MAGMA,
        cv2.COLORMAP_INFERNO,
        cv2.COLORMAP_VIRIDIS,
        cv2.COLORMAP_DEEPGREEN,
        cv2.COLORMAP_HOT,
        cv2.COLORMAP_SPRING,
        cv2.COLORMAP_PLASMA,
        cv2.COLORMAP_SUMMER,
        cv2.COLORMAP_WINTER,
        cv2.COLORMAP_TWILIGHT,
        cv2.COLORMAP_TURBO,
        cv2.COLORMAP_PINK,
        cv2.COLORMAP_PARULA,
        cv2.COLORMAP_BONE,
    ]

    def __init__(self, canvas: Any, tile_size: int) -> None:
        """Initialize the theme manager."""
        self.canvas: Any = canvas
        self.tile_size = tile_size

        self.themes: dict[str, LoadedTheme] = {}
        self.raw_themes: dict[str, RawTheme] = {}
        self.current: LoadedTheme | None = None

        self.load_all()

    def get_list_themes(self) -> list[str]:
        """Return the available theme directory names."""
        directory_path = os.path.join(
            os.getcwd(),
            "Assets",
        )

        return [
            name
            for name in os.listdir(directory_path)
            if os.path.isdir(
                os.path.join(directory_path, name)
            )
        ]

    def load_all(self) -> None:
        """Load every available graphical theme."""
        theme_names = self.get_list_themes()

        for theme_name in theme_names:
            self.themes[theme_name] = {}
            self.raw_themes[theme_name] = {}

            for filename in self.FILES:
                try:
                    image_array = self.img_array(
                        theme_name,
                        filename,
                    )

                except FileNotFoundError:
                    #   sys.stderr.write(
                    #       f"{filename} not found. "
                    #       "Generating a random image instead.\n"
                    #   )

                    option = random.randint(0, 2)

                    if option == 2:
                        image_array = (
                            self.generate_brushed_texture()
                        )
                    elif option == 1:
                        image_array = (
                            self.generate_cellular_texture()
                        )
                    else:
                        image_array = (
                            self.generate_plane_color()
                        )

                self.raw_themes[theme_name][
                    filename
                ] = image_array

                loaded_image = self.canvas.load_image(
                    image_array
                )

                self.themes[theme_name][
                    filename
                ] = loaded_image

        if "default" not in self.themes:
            raise ValueError(
                "The default graphical theme was not found"
            )

        self.current = self.themes["default"]

    def img_array(
        self,
        theme: str,
        filename: str,
        resizing: bool = False,
    ) -> ImageArray:
        """Load an image as a BGRA NumPy array."""
        image_path = os.path.join(
            "Assets",
            theme,
            filename,
        )

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(image_path)

        image_bgra = cv2.cvtColor(
            image,
            code=cv2.COLOR_BGR2BGRA,
        )

        if resizing or self.tile_size != 32:
            resized_image = cv2.resize(
                image_bgra,
                (self.tile_size, self.tile_size),
            )

            return np.asarray(
                resized_image,
                dtype=np.uint8,
            )

        return np.asarray(
            image_bgra,
            dtype=np.uint8,
        )

    def set_theme(self, name: str) -> None:
        """Select a loaded theme by name."""
        if name not in self.themes:
            raise ValueError(
                f"Unknown theme: {name}"
            )

        self.current = self.themes[name]

    def get_image(self, name: Any) -> Any:
        """Return a loaded image from the current theme."""
        if self.current is None:
            raise RuntimeError(
                "No graphical theme is currently selected"
            )

        return self.current[name]

    def get_img_raw(self, name: Any) -> ImageArray:
        """Return a raw image from the current theme."""
        if self.current is None:
            raise RuntimeError(
                "No graphical theme is currently selected"
            )

        current_theme_name = next(
            (
                theme_name
                for theme_name, theme in self.themes.items()
                if theme is self.current
            ),
            None,
        )

        if current_theme_name is None:
            raise RuntimeError(
                "Current graphical theme could not be found"
            )

        return self.raw_themes[
            current_theme_name
        ][name]

    def generate_plane_color(self) -> ImageArray:
        """Generate a random solid-colour texture."""
        image = np.zeros(
            (
                self.tile_size,
                self.tile_size,
                3,
            ),
            dtype=np.uint8,
        )

        blue = random.randint(0, 255)
        green = random.randint(0, 255)
        red = random.randint(0, 255)

        image[:, :, 0] = blue
        image[:, :, 1] = green
        image[:, :, 2] = red

        image_bgra = cv2.cvtColor(
            image,
            code=cv2.COLOR_BGR2BGRA,
        )

        return np.asarray(
            image_bgra,
            dtype=np.uint8,
        )

    def generate_cellular_texture(self) -> ImageArray:
        """Generate a random cellular texture."""
        x_coordinates = np.arange(
            self.tile_size
        )
        y_coordinates = np.arange(
            self.tile_size
        )

        grid_x, grid_y = np.meshgrid(
            x_coordinates,
            y_coordinates,
        )

        pixel_coordinates = np.stack(
            (grid_x, grid_y),
            axis=-1,
        )

        number_of_points = int(
            np.random.randint(40, 100)
        )

        points = np.column_stack(
            (
                np.random.randint(
                    0,
                    self.tile_size,
                    number_of_points,
                ),
                np.random.randint(
                    0,
                    self.tile_size,
                    number_of_points,
                ),
            )
        )

        differences = (
            pixel_coordinates[:, :, np.newaxis, :]
            - points[np.newaxis, np.newaxis, :, :]
        )

        distances = np.linalg.norm(
            differences,
            axis=-1,
        )

        minimum_distances = np.min(
            distances,
            axis=-1,
        )

        grayscale_image = np.clip(
            minimum_distances * 5,
            0,
            255,
        ).astype(np.uint8)

        chosen_colormap = random.choice(
            self.COLORMAPS
        )

        color_texture = cv2.applyColorMap(
            grayscale_image,
            chosen_colormap,
        )

        image_bgra = cv2.cvtColor(
            color_texture,
            code=cv2.COLOR_BGR2BGRA,
        )

        return np.asarray(
            image_bgra,
            dtype=np.uint8,
        )

    def generate_brushed_texture(self) -> ImageArray:
        """Generate a random brushed-metal texture."""
        noise = np.random.randint(
            100,
            180,
            (
                self.tile_size,
                self.tile_size,
            ),
            dtype=np.uint8,
        )

        kernel_size = 30

        kernel = np.zeros(
            (kernel_size, kernel_size),
            dtype=np.float32,
        )

        middle_row = (kernel_size - 1) // 2

        kernel[middle_row, :] = np.ones(
            kernel_size,
            dtype=np.float32,
        )

        kernel /= kernel_size

        filtered_image = cv2.filter2D(
            noise,
            -1,
            kernel,
        )

        brushed_image = np.asarray(
            filtered_image,
            dtype=np.uint8,
        )

        normalized_image = np.empty_like(
            brushed_image
        )

        cv2.normalize(
            brushed_image,
            normalized_image,
            0.0,
            255.0,
            cv2.NORM_MINMAX,
        )

        chosen_colormap = random.choice(
            self.COLORMAPS
        )

        color_texture = cv2.applyColorMap(
            normalized_image,
            chosen_colormap,
        )

        image_bgra = cv2.cvtColor(
            color_texture,
            code=cv2.COLOR_BGR2BGRA,
        )

        return np.asarray(
            image_bgra,
            dtype=np.uint8,
        )
