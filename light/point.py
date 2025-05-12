from imports.common import *

from model.ray import Ray


@ti.dataclass
class Point:
    color: vec3  # type: ignore
    position: vec3  # type: ignore

    @ti.func
    def get_ray(self, point: vec3):  # type: ignore
        return Ray(point, (self.position - point).normalized())
