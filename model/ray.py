import taichi as ti
from taichi.math import vec3

from .hit_info import HitInfo


NO_COLOR = vec3(1, 0, 1)


@ti.dataclass
class Ray:
    origin: vec3  # type: ignore
    direction: vec3  # type: ignore

    def __init__(self, origin: vec3, direction: vec3):  # type: ignore
        self.origin = origin
        self.direction = direction

    @ti.func
    def cast(self, objects: ti.template()) -> HitInfo:  # type: ignore
        color = NO_COLOR
        point = self.origin
        normal = self.direction
        hit = False

        nearest = ti.math.inf
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(self)
            if coef > 0 and coef < nearest:
                nearest = coef
                hit = True

                color = objects[i].color
                point = self.origin + self.direction * coef
                normal = objects[i].normal(point)

        return HitInfo(hit, point, normal, color)
