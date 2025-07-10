from abc import ABC, abstractmethod

from ..transform import Transform


class Lens(ABC):

    transform: Transform

    @abstractmethod
    def render(self, pixels, objects): ...
