from imports.common import *

from camera.ray import Ray


@ti.dataclass
class BoundingBox:
    min_point: vec3  # type: ignore
    max_point: vec3  # type: ignore

    def intersects(self, ray: Ray) -> bool:  # type: ignore
        return False
