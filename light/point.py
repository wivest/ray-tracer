from imports.common import *

from model.ray import Ray
from sky.colored import Colored


@ti.dataclass
class Point:
    color: vec3  # type: ignore
    position: vec3  # type: ignore

    @ti.func
    def is_visible(self, point: vec3, objects: ti.template()) -> bool:  # type: ignore
        ray = Ray(point, (self.position - point).normalized())
        hit_info = ray.cast(objects, Colored(vec3(0)), vec3(0))  # type: ignore
        return hit_info.hit
