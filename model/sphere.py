import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

from .ray import Ray


@ti.dataclass
class Sphere:
    radius: f32  # type: ignore
    origin: vec3  # type: ignore
    color: vec3  # type: ignore

    def __init__(self, r: f32, origin: vec3, color: vec3 = Vector((1, 1, 1), f32)):  # type: ignore
        self.radius = r
        self.origin = origin
        self.color = color

    @ti.func
    def intersects(self, ray: Ray) -> bool:  # type: ignore
        line = ray.direction
        diff = ray.origin - self.origin

        solution = False
        dot = ti.math.dot(line, diff)
        determinant = dot * dot - diff.norm_sqr() + self.radius * self.radius
        if determinant >= 0:
            coef = -dot + ti.math.sqrt(determinant)
            solution = coef > 0
        return solution
