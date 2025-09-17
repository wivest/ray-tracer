from imports.common import *

from camera.ray import Ray


@ti.dataclass
class Sun:
    color: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def get_ray(self, point: vec3) -> Ray:  # type: ignore
        return Ray(point, -self.direction.normalized())
