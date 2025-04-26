import taichi as ti
from taichi.math import vec3

from .sky import Sky
from .hit_info import HitInfo
from .material import Material


@ti.dataclass
class Ray:
    origin: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def cast(self, objects: ti.template(), sky: Sky) -> HitInfo:  # type: ignore
        sky_color = sky.get(self.direction)

        material = Material()
        point = self.origin
        normal = self.direction
        hit = False

        nearest = ti.math.inf
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(self)
            if coef > 0 and coef < nearest:
                nearest = coef
                hit = True

                material = objects[i].material
                point = self.origin + self.direction * coef
                normal = objects[i].normal(point)

        if not hit:
            material.diffuse = sky_color  # type: ignore

        return HitInfo(hit, point, normal, material)
