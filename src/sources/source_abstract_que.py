from typing import Optional

from numpy import ndarray

from sources.image_que import ImageQue
from sources.source_abstract import AbstractSource


class AbstractQueSource(AbstractSource):
    def __init__(self) -> None:
        super().__init__()
        self._image_que: Optional[ImageQue] = None

    @property
    def ready(self) -> bool:
        return self._image_que is not None

    def init_que(self):
        self._image_que = ImageQue(width=self.width, height=self.height)

    def get_frame(self) -> ndarray:
        if self._image_que is None:
            raise AttributeError("Image Que was not created before accessing it")
        return self._image_que.dequeue()
