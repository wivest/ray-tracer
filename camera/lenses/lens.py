from abc import ABC, abstractmethod

from imports.common import *

from ..transform import Transform


class Lens(ABC):

    transform: Transform

    @abstractmethod
    def render(
        self, pixels: MatrixField, triangles: StructField, bvhs: StructField
    ): ...
