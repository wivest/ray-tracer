from imports.common import *

from model.material import Material


@ti.dataclass
class HitInfo:
    hit: bool
    point: vec3  # type: ignore
    normal: vec3  # type: ignore
    material: Material  # type: ignore
