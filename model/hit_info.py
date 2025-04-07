import taichi as ti
from taichi.math import vec3

from .material import Material


@ti.dataclass
class HitInfo:
    hit: bool
    point: vec3  # type: ignore
    normal: vec3  # type: ignore
    material: Material  # type: ignore

    def __init__(self, hit: bool, point: vec3, normal: vec3, material: Material):  # type: ignore
        self.hit = hit
        self.point = point
        self.normal = normal
        self.material = material
