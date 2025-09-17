from imports.common import *

from .point import Point
from .sun import Sun
from camera.ray import Ray


@ti.dataclass
class LightUnion:
    select: int
    point: Point  # type: ignore
    sun: Sun  # type: ignore

    @ti.func
    def get_ray(self, point: vec3) -> Ray:  # type: ignore
        ray = self.point.get_ray(point)
        if self.select == 1:
            ray = self.sun.get_ray(point)
        return ray

    @ti.func
    def get_color(self) -> vec3:  # type: ignore
        color = self.point.color
        if self.select == 1:
            color = self.sun.color
        return color
