import taichi as ti
from taichi.math import vec3


@ti.dataclass
class Ray:
    origin: vec3  # type: ignore
    direction: vec3  # type: ignore

    def __init__(self, origin: vec3, direction: vec3):  # type: ignore
        self.origin = origin
        self.direction = direction


@ti.dataclass
class HitInfo:
    reflected: Ray  # type: ignore
    color: vec3  # type: ignore
    hit: bool

    def __init__(self, reflected: Ray, color: vec3, hit: bool):  # type: ignore
        self.reflected = reflected
        self.color = color
        self.hit = hit
