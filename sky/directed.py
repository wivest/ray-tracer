import taichi as ti

from math import inf
from taichi import f32, Vector
from taichi.math import vec3


FILTER = Vector((1, 1, 1), f32)


@ti.dataclass
class Directed:
    @ti.func
    def get(self, direction: vec3) -> Vector:  # type: ignore
        direction = ti.math.clamp(direction, vec3(0), vec3(inf))
        return FILTER * direction
