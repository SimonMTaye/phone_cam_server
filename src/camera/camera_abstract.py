from abc import abstractmethod
from time import sleep
from numpy import ndarray
from contextlib import AbstractContextManager


class AbstractCamera(AbstractContextManager):
    def __init__(self, width: int, height: int, fps: int = 24) -> None:
        self.width = width
        self.height = height
        self.fps = fps

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return exc_type == None

    def wait_for_next_frame(self):
        sleep(1 / self.fps)

    @abstractmethod
    def send(self, frame: ndarray, *, changed=True):
        assert frame.shape == (self.height, self.width, 4)
        pass

    @abstractmethod
    def close(self):
        pass