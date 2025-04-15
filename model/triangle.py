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
        coefficient = -1.0

        side1 = self.v2 - self.v1
        side2 = self.v3 - self.v1
        normal = ti.math.cross(side1, side2)

        if ti.math.dot(ray.direction, normal) != 0.0:
            vo = ray.origin - self.v1
            numerator = ti.math.dot(vo, normal)
            denominator = ti.math.dot(ray.direction, normal)
            coefficient = -numerator / denominator
        return coefficient
