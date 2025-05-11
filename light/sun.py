from imports.common import *

from model.ray import Ray


@ti.dataclass
class Sun:
    color: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def is_visible(self, point: vec3, objects: ti.template()) -> bool:  # type: ignore
        ray = Ray(point, -self.direction.normalized())
        hit_info = ray.cast(objects)  # type: ignore
        return not hit_info.hit
