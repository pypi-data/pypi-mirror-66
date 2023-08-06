import numpy as np

from dlds.decoder.dlds_decoder import *
import cv2


class OpencvDecoder(DLDSDecoder):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, image_bytes):
        buffer = np.asarray(bytearray(image_bytes), dtype=np.uint8)
        image = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def __reduce__(self):
        return (OpencvDecoder, ())

    @staticmethod
    def get_file_extensions() -> List[str]:
        return ['bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'pdm', 'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif']
