from typing import Any, Optional, Tuple
from threading import Lock
from copy import copy

from numpy import ndarray 

from sources.image_utils import process_image, get_image_object, valid_frame, blank_image


class ImageQue:

    _list_lock = Lock()

    def __init__(self, width, height, max_size: int = 3) -> None:
        self._list = []
        self._max_size = max_size
        self._img_height = height
        self._img_width = width

    def queue(self, data: Any):
        image = get_image_object(data)
        frame = process_image(data, self._img_width, self._img_height)
        if valid_frame(frame, self._img_height, self._img_width):
            with self._list_lock:
                if len(self._list) >= self._max_size:
                    self._list.pop(0)
                self._list.append(frame)

    def dequeue(self) -> ndarray:
        with self._list_lock:
            if len(self._list) == 0:
                return blank_image(self._img_width, self._img_height)
            elif len(self._list) == 1:
                data = copy(self._list[0])
                return data
            else:
                data = self._list.pop(0)
                assert isinstance(data, ndarray)
                return data

        
    
    