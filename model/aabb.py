from imports.common import *

from camera.ray import Ray


@ti.dataclass
class AABB:
    min_point: vec3  # type: ignore
    max_point: vec3  # type: ignore

    @ti.func
    def intersects(self, ray: Ray) -> bool:  # type: ignore
        low = (self.min_point - ray.origin) / ray.direction
        high = (self.max_point - ray.origin) / ray.direction

        close = ti.math.min(low, high)
        far = ti.math.max(low, high)

        close_fac = ti.math.max(close.x, close.y, close.z)
        far_fac = ti.math.min(far.x, far.y, far.z)

        return far_fac > 0 and close_fac <= far_fac

    @ti.func
    def distance(self, ray: Ray) -> float:  # type: ignore
        low = (self.min_point - ray.origin) / ray.direction
        high = (self.max_point - ray.origin) / ray.direction

        close = ti.math.min(low, high)
        far = ti.math.max(low, high)

        close_fac = ti.math.max(close.x, close.y, close.z)
        far_fac = ti.math.min(far.x, far.y, far.z)

        hit = far_fac > 0 and close_fac <= far_fac
        distance = (close_fac if close_fac >= 0 else far_fac) if hit else ti.math.inf
        return distance
