from imports.common import *

from math import inf


FILTER = Vector((1, 1, 1), f32)


@ti.dataclass
class Directed:
    @ti.func
    def get(self, direction: vec3) -> Vector:  # type: ignore
        direction = ti.math.clamp(direction, vec3(0), vec3(inf))
        return FILTER * direction
