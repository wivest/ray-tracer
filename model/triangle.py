import taichi as ti

from taichi import f32
from taichi.math import vec3

from .ray import Ray
from .material import Material


@ti.dataclass
class Triangle:
    a: vec3  # type: ignore
    b: vec3  # type: ignore
    c: vec3  # type: ignore
    material: Material  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> f32:  # type: ignore
        solution = -1.0

        edgeAB = self.b - self.a
        edgeAC = self.c - self.a
        ray_dir = -ray.direction
        det = self._det(ray_dir, edgeAB, edgeAC)

        inv_det = 1.0 / det
        vecAO = ray.origin - self.a

        t = inv_det * self._det(vecAO, edgeAB, edgeAC)
        u = inv_det * self._det(ray_dir, vecAO, edgeAC)
        v = inv_det * self._det(ray_dir, edgeAB, vecAO)

        if det != 0.0 and 0.0 < u + v and u + v < 1.0 and u * v > 0.0 and t > 0:
            solution = t

        return solution

    @ti.func
    def normal(self, point: vec3) -> vec3:  # type: ignore
        return ti.math.cross(self.b - self.a, self.c - self.a)

    @ti.func
    def _det(self, col1: vec3, col2: vec3, col3: vec3) -> f32:  # type: ignore
        cross = ti.math.cross(col2, col3)
        return ti.math.dot(col1, cross)
