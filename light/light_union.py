from imports.common import *

from .point import Point
from .sun import Sun


@ti.dataclass
class LightUnion:
    select: int
    point: Point  # type: ignore
    sun: Sun  # type: ignore

    @ti.func
    def sample_light(self, point: vec3, normal: vec3, triangles: ti.template(), bvhs: ti.template()) -> vec3:  # type: ignore
        color = self.point.sample_light(point, normal, triangles, bvhs)
        if self.select == 1:
            color = self.sun.sample_light(point, normal, triangles, bvhs)
        return color
