from abc import ABC, abstractmethod


class Lens(ABC):

    @abstractmethod
    def render(self, pixels, objects): ...
