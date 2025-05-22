from imports.common import *

from .ray import Ray
from .material import Material


# treshhold
TH_ZERO = 0.001


@ti.dataclass
class Triangle:
    a: vec3  # type: ignore
    b: vec3  # type: ignore
    c: vec3  # type: ignore
    material: Material  # type: ignore
    normal: vec3  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> f32:  # type: ignore
        solution = -1.0

        edgeAB = self.b - self.a
        edgeAC = self.c - self.a
        inv_ray_dir = -ray.direction
        det = self._det(inv_ray_dir, edgeAB, edgeAC)

        inv_det = 1.0 / det
        vecAO = ray.origin - self.a

        sol = inv_det * self._det(vecAO, edgeAB, edgeAC)
        ab = inv_det * self._det(inv_ray_dir, vecAO, edgeAC)
        ac = inv_det * self._det(inv_ray_dir, edgeAB, vecAO)

        if (
            det != 0.0
            and -TH_ZERO <= ab + ac
            and ab + ac <= 1 + TH_ZERO
            and ab > -TH_ZERO
            and ac > -TH_ZERO
            and sol > 0
        ):
            solution = sol

        return solution

    @ti.func
    def update_normal(self):  # type: ignore
        self.normal = ti.math.cross(self.b - self.a, self.c - self.a).normalized()

    @ti.func
    def _det(self, col1: vec3, col2: vec3, col3: vec3) -> f32:  # type: ignore
        cross = ti.math.cross(col2, col3)
        return ti.math.dot(col1, cross)
