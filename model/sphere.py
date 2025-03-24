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
        to_center = self.origin - ray.origin
        dist = ti.math.cross(line, to_center).norm() / line.norm()
        dot = ti.math.dot(line, to_center)
        return dist < self.radius and dot >= 0
