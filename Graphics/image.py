import numpy as np


class ImgData():
    """ Generate image objets to send into graphic library """
    def __init__(self):
        self.id = None
        self.width: int | None = None
        self.height: int | None = None
        self.data: np.ndarray = np.asarray(None)
        self.bytesPP = None     # Bytes per Pixel
        self.bytesPL = None     # Bytes per Line (stride)
        self.format = None
