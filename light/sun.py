from imports.common import *

from model.ray import Ray
from sky.colored import Colored


@ti.dataclass
class Sun:
    color: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def is_visible(self, point: vec3, objects: ti.template()) -> bool:  # type: ignore
        ray = Ray(point, self.direction.normalized())
        hit_info = ray.cast(objects, Colored(vec3(0)), vec3(0))  # type: ignore
        return not hit_info.hit
