import taichi as ti
from taichi.math import vec3


@ti.dataclass
class HitInfo:
    hit: bool
    point: vec3  # type: ignore
    normal: vec3  # type: ignore
    color: vec3  # type: ignore

    def __init__(self, hit: bool, point: vec3, normal: vec3, color: vec3):  # type: ignore
        self.hit = hit
        self.point = point
        self.normal = normal
        self.color = color
