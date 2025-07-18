from imports.common import *

from camera.ray import Ray


@ti.dataclass
class BoundingBox:
    min_point: vec3  # type: ignore
    max_point: vec3  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> bool:  # type: ignore
        low = (self.min_point - ray.origin) / ray.direction
        high = (self.max_point - ray.origin) / ray.direction

        close = ti.math.max(low.x, low.y, low.z)
        far = ti.math.max(high.x, high.y, high.z)

        return close > 0 and close <= high
