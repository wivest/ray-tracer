from imports.common import *

from .hit_info import HitInfo
from model.material import Material


TRESHHOLD = 0.001


@ti.dataclass
class Ray:
    origin: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def cast(self, objects: ti.template()) -> HitInfo:  # type: ignore
        point = self.origin
        normal = vec3(0)
        material = Material()
        hit = False

        nearest = ti.math.inf
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(self)
            if coef > TRESHHOLD and coef < nearest:
                nearest = coef
                hit = True

                material = objects[i].material
                point = self.origin + self.direction * coef
                normal = objects[i].normal

        return HitInfo(hit, point, normal, material)
