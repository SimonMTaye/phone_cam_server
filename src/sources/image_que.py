from io import BytesIO
from typing import Any, Optional
from threading import Lock
from copy import copy

from PIL import Image
from numpy import ndarray, asarray_chkfinite, zeros, uint8

from .linked_list import LinkedList


class ImageQue:

    _list_lock = Lock()

    def __init__(self, max_size: int = 3, *, width = 1920, height = 1080) -> None:
        self._list = []
        self._max_size = max_size
        self._img_height = 1080
        self._img_width = 1920

    def queue(self, data: Any):
        frame = self.process_image(data, self._img_width, self._img_height)
        if self.valid_frame(frame, self._img_height, self._img_width):
            with self._list_lock:
                if len(self._list) >= self._max_size:
                    self._list.pop(0)
                self._list.append(frame)

    def dequeue(self) -> ndarray:
        with self._list_lock:
            if len(self._list) == 0:
                return zeros((self._img_width, self._img_height, 4), uint8)
            elif len(self._list) == 1:
                data = copy(self._list[0])
                return data
            else:
                data = self._list.pop(0)
                assert isinstance(data, ndarray)
                return data


    @staticmethod
    def process_image(data, width: Optional[int] = None, height: Optional[int] = None):
        img_data = BytesIO(data)
        img = Image.open(img_data)
        img = img.convert("RGBA")
        if width and height:
            img = img.resize((width, height))
        return asarray_chkfinite(img)

    @staticmethod
    def valid_frame(frame: ndarray, height: int, width: int) -> bool:
        # print(f"Image dimen: {frame.shape}")
        # print(f"Valid dimen:  ({height}, {width}, 4)")
        return frame.shape[0] == height and frame.shape[1] == width
