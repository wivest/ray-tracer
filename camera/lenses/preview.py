from imports.common import *

from .lens import Lens
from ..tonemapping import aces
from ..transform import Transform
from ..ray import Ray


@ti.data_oriented
class Preview(Lens):

    sky = vec3(0.5, 0.5, 0.5)

    def __init__(self, size: tuple[int, int], angle: float, transform: Transform):
        self.fov: float = size[1] / ti.tan(angle / 2)
        self.transform = transform

    @ti.kernel
    def render(self, pixels: ti.template(), objects: ti.template()):  # type: ignore
        center_x = pixels.shape[0] / 2
        center_y = pixels.shape[1] / 2
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self._get_color(ray, objects)
            pixels[x, y] = aces(incoming_light)

    @ti.func
    def _get_color(self, ray: Ray, objects: ti.template()) -> Vector:  # type: ignore
        incoming_light = self.sky

        hit_info = ray.cast(objects)
        if hit_info.hit:
            sin = ti.abs(ti.math.dot(ray.direction, hit_info.normal))
            incoming_light = sin * (
                hit_info.material.emission + hit_info.material.diffuse
            )

        return incoming_light
