from abc import ABC, abstractmethod
from typing import Optional
from numpy import ndarray

# TODO Figure out logging
# TODO Context manager for sources

class AbstractSource(ABC):
    def __init__(self) -> None:
        self._width: Optional[int] = None
        self._height: Optional[int] = None

    @property
    @abstractmethod
    def ready(self) -> bool:
        raise NotImplementedError()

    @property
    def width(self) -> int:
        if self._width is None:
            raise AttributeError("Width was accessed before it was set")
        return self._width

    @property
    def height(self) -> int:
        if self._height is None:
            raise AttributeError("Height was accessed before it was set")
        return self._height

    @abstractmethod
    def get_frame(self) -> ndarray:
        raise NotImplementedError()
