import taichi as ti
from taichi.math import vec3

from .sky import Sky
from .hit_info import HitInfo
from .material import Material


@ti.dataclass
class Ray:
    origin: vec3  # type: ignore
    direction: vec3  # type: ignore

    def __init__(self, origin: vec3, direction: vec3):  # type: ignore
        self.origin = origin
        self.direction = direction

    @ti.func
    def cast(self, objects: ti.template(), sky: Sky) -> HitInfo:  # type: ignore
        color = sky.get(self.direction)
        specular = 1.0
        point = self.origin
        normal = self.direction
        hit = False

        nearest = ti.math.inf
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(self)
            if coef > 0 and coef < nearest:
                nearest = coef
                hit = True

                color = objects[i].material.color
                specular = objects[i].material.specular
                point = self.origin + self.direction * coef
                normal = objects[i].normal(point)

        return HitInfo(
            hit,
            point,
            normal,
            Material(color, specular),
        )
