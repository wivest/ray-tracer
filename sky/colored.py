import taichi as ti

from taichi import Vector
from taichi.math import vec3


@ti.dataclass
class Colored:
    color: vec3  # type: ignore

    @ti.func
    def get(self, direction: vec3) -> Vector:  # type: ignore
        return self.color
