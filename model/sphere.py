from imports.common import *

from .material import Material

from camera.ray import Ray


@ti.dataclass
class Sphere:
    radius: f32  # type: ignore
    origin: vec3  # type: ignore
    material: Material  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> f32:  # type: ignore
        line = ray.direction
        diff = ray.origin - self.origin

        solution = -1.0
        dot = ti.math.dot(line, diff)
        determinant = dot * dot - diff.norm_sqr() + self.radius * self.radius
        if determinant >= 0:
            coef = -dot - ti.math.sqrt(determinant)
            if coef >= 0:
                solution = coef
        return solution

    @ti.func
    def normal(self, point: vec3) -> vec3:  # type: ignore
        return (point - self.origin).normalized()
