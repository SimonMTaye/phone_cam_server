from abc import ABC, abstractmethod
from typing import Optional
from numpy import ndarray

# TODO Figure out logging
class AbstractSource(ABC):

    def __init__(self) -> None:
        self.__width : Optional[int] = None
        self.__height : Optional[int] = None
        
    @property
    @abstractmethod
    def ready(self) -> bool:
        raise NotImplementedError()

    @property
    def width(self) -> int:
        if self.__width is None:
            raise AttributeError("Width was accessed before it was set")
        return self.__width

    @property
    def height(self) -> int:
        if self.__height is None:
            raise AttributeError("Height was accessed before it was set")
        return self.__height

    @abstractmethod
    def get_frame(self) -> ndarray:
        raise NotImplementedError()