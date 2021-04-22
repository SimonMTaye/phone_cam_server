from abc import ABC, abstractmethod
from typing import Dict

from sources.source_abstract import AbstractSource
from collections import namedtuple

ParamInfo = namedtuple("Param", ["type", "description", "required"])

# For sources that need a while to initialize before being used

# Used as a mixin class
class FactoryMixin(ABC):
    @staticmethod
    @abstractmethod
    def create(**kwargs) -> AbstractSource:
        return NotImplementedError()

    @staticmethod
    @abstractmethod
    def parameters() -> Dict[str, ParamInfo]:
        return NotImplementedError()
