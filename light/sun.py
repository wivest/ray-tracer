from imports.common import *

from camera.ray import Ray


@ti.dataclass
class Sun:
    color: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def sample_light(self, point: vec3, normal: vec3, triangles: ti.template(), bvhs: ti.template()) -> vec3:  # type: ignore
        ray = Ray(point, -self.direction.normalized())
        visible = Vector((0.0, 0.0, 0.0))

        sin = ti.math.dot(ray.direction, normal)  # type: ignore
        if not ray.cast(triangles, bvhs).hit:  # type: ignore
            visible += sin * self.color  # type: ignore

        return visible
