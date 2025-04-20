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
        inv_ray_dir = -ray.direction
        det = self._det(inv_ray_dir, edgeAB, edgeAC)

        inv_det = 1.0 / det
        vecAO = ray.origin - self.a
        front = ti.math.dot(inv_ray_dir, self.normal(vec3(0, 0, 0))) > 0

        sol = inv_det * self._det(vecAO, edgeAB, edgeAC)
        ab = inv_det * self._det(inv_ray_dir, vecAO, edgeAC)
        ac = inv_det * self._det(inv_ray_dir, edgeAB, vecAO)

        if (
            det != 0.0
            and 0.0 < ab + ac
            and ab + ac < 1.0
            and ab * ac > 0.0
            and sol > 0
            and front
        ):
            solution = sol

        return solution

    @ti.func
    def normal(self, point: vec3) -> vec3:  # type: ignore
        return ti.math.cross(self.b - self.a, self.c - self.a).normalized()

    @ti.func
    def _det(self, col1: vec3, col2: vec3, col3: vec3) -> f32:  # type: ignore
        cross = ti.math.cross(col2, col3)
        return ti.math.dot(col1, cross)
