from typing import Optional
from os import path

from numpy import ndarray, asarray_chkfinite, zeros, uint8
from PIL import Image

from .source import AbstractSource

#To be Deleted
class ImageFileSource(AbstractSource):
    def get_frame(self) -> ndarray:
        if self._image_data is None:
            self._image_data = zeros((self.width, self.height, 4), uint8)
        return self._image_data

    @classmethod
    def create(cls, image_path: Optional[str] = None) -> "ImageFileSource":
        if image_path:
            if not cls.valid_image(image_path):
                raise ValueError("Image path is invalid")
            img = Image.open(image_path)
            source = cls(width=img.width, height=img.height, fps=24)
            if not source._set_image_data(asarray_chkfinite(img, dtype=uint8)):
                raise ValueError("Error using image")
        else:
            source = cls(width=1920, height=1080, fps=24)
        return source

    def _set_image_data(self, data: ndarray) -> bool:
        shape = data.shape
        if shape[0] == self.width and shape[1] == self.height:
            self._image_data = data
            return True
        else:
            return False

    @staticmethod
    def valid_image(image_path: str) -> bool:
        return path.exists(image_path)
