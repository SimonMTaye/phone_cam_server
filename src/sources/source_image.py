from typing import Dict, Optional

from numpy import ndarray, asarray_chkfinite
from PIL import Image

from sources.source_abstract import AbstractSource 
from sources.factory import FactoryMixin, ParamInfo


class ImageFileSource(AbstractSource, FactoryMixin):
    
    
    def __init__(self) -> None:
        super().__init__()
        self.__image_data: Optional[ndarray] = None
    
    @property
    def ready(self):
        return self.__image_data is not None
        
    def read_image(self, path: str):
        self.__image_data = asarray_chkfinite(Image.open(path))
        
    def get_frame(self):
        if self.__image_data == None:
            raise AttributeError("Image Data is empty. Call read_image before using this source to avoid this")
        return self.__image_data
        
    @staticmethod
    def parameters()-> Dict[str, ParamInfo]:
        return {"path": ParamInfo(str, "Path to image file", True)}
    
    @staticmethod
    def create(**kwargs) -> "ImageFileSource":
        try:
            path = kwargs["path"]
            source = ImageFileSource()
            source.read_image(path)
            return source
        except KeyError:
            raise ValueError("Required function parameters not passed")
