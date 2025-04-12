import taichi as ti

from taichi import f32
from taichi.math import vec3

from .ray import Ray


@ti.dataclass
class Triangle:
    v1: vec3  # type: ignore
    v2: vec3  # type: ignore
    v3: vec3  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> f32:  # type: ignore
        return -1.0
