import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

from .ray import Ray
from .material import Material


@ti.dataclass
class Sphere:
    radius: f32  # type: ignore
    origin: vec3  # type: ignore
    material: Material  # type: ignore

    def __init__(self, r: f32, origin: vec3, material: Material):  # type: ignore
        self.radius = r
        self.origin = origin
        self.material = material

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
