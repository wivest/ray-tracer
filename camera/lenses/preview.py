from imports.common import *

from .lens import Lens
from ..tonemapping import aces
from ..transform import Transform
from ..ray import Ray


@ti.data_oriented
class Preview(Lens):

    sky = vec3(0.5, 0.5, 0.5)
    hit_color = vec3(1.0, 1.0, 1.0)

    def __init__(self, size: tuple[int, int], angle: float, transform: Transform):
        self.fov: float = size[1] / ti.tan(angle / 2)
        self.transform = transform

    def render(self, pixels: MatrixField, triangles: StructField, bvhs: StructField):
        self._render_sample(pixels, triangles, bvhs)

    @ti.kernel
    def _render_sample(self, pixels: ti.template(), triangles: ti.template(), bvhs: ti.template()):  # type: ignore
        center_x = pixels.shape[0] / 2
        center_y = pixels.shape[1] / 2
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self._get_color(ray, triangles, bvhs)
            pixels[x, y] = aces(incoming_light)

    @ti.func
    def _get_color(self, ray: Ray, triangles: ti.template(), bvhs: ti.template()) -> Vector:  # type: ignore
        incoming_light = self.sky

        hit_info = self._cast_ray(ray, triangles, bvhs)

        if hit_info.hit:  # type: ignore
            sin = ti.abs(ti.math.dot(ray.direction, hit_info.normal))  # type: ignore
            incoming_light = sin * self.hit_color

        return incoming_light
