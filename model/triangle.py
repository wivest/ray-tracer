import taichi as ti

from taichi import f32
from taichi.math import vec3

from .ray import Ray


@ti.dataclass
class Triangle:
    a: vec3  # type: ignore
    b: vec3  # type: ignore
    c: vec3  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> f32:  # type: ignore
        solution = -1.0

        edgeAB = self.b - self.a
        edgeAC = self.c - self.a
        det = self._det(ray.direction, edgeAB, edgeAC)

        inv_det = 1.0 / det
        vecAO = ray.origin - self.a

        t = inv_det * self._det(vecAO, edgeAB, edgeAC)
        u = inv_det * self._det(ray.direction, vecAO, edgeAC)
        v = inv_det * self._det(ray.direction, edgeAB, vecAO)

        if det != 0.0 and 0.0 < u + v and u + v > 1.0:
            solution = t

        return solution

    @ti.func
    def _det(self, col1: vec3, col2: vec3, col3: vec3) -> f32:  # type: ignore
        cross = ti.math.cross(col2, col3)
        return ti.math.dot(col1, cross)
