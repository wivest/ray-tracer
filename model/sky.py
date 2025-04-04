import taichi as ti

from taichi import f32, Vector
from taichi.math import vec3


FILTER = Vector((1, 1, 1), f32)


@ti.dataclass
class Sky:
    @ti.func
    def get(self, direction: vec3) -> Vector:  # type: ignore
        return FILTER * direction
