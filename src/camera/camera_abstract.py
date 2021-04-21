from abc import abstractmethod
from typing import Optional
from numpy import ndarray
from contextlib import AbstractContextManager


class AbstractCamera(AbstractContextManager):
    def __init__(self, width: int, height: int, fps: int = 24) -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self._last_frame: Optional[ndarray] = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return exc_type == None

    @abstractmethod
    def send(self, frame: ndarray, *, changed=True):
        assert frame.shape == (self.height, self.width, 4)
        self._last_frame = frame
        pass

    @abstractmethod
    def close(self):
        pass
