import taichi as ti

from taichi import f32
from taichi.math import vec3

from .material import Material


@ti.dataclass
class HitInfo:
    hit: bool
    point: vec3  # type: ignore
    normal: vec3  # type: ignore
    material: Material  # type: ignore
    sin: f32  # type: ignore
