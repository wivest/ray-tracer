import taichi as ti
from taichi.math import vec3

from .ray import Ray


@ti.dataclass
class HitInfo:
    reflected: Ray  # type: ignore
    color: vec3  # type: ignore
    hit: bool

    def __init__(self, reflected: Ray, color: vec3, hit: bool):  # type: ignore
        self.reflected = reflected
        self.color = color
        self.hit = hit
