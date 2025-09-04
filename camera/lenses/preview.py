from imports.common import *

from .lens import Lens
from ..transform import Transform
from ..ray import Ray


@ti.data_oriented
class Preview(Lens):

    sky = vec3(0.5, 0.5, 0.5)
    hit_color = vec3(1.0, 1.0, 1.0)

    def __init__(self, size: tuple[int, int], transform: Transform):
        self.fov: float = size[1] / ti.tan(transform.angle)
        self.transform = transform

    def render(self, pixels: MatrixField, triangles: StructField, bvhs: StructField):
        self._render_sample(pixels, triangles, bvhs)

    @ti.func
    def _get_color(self, ray: Ray, triangles: ti.template(), bvhs: ti.template()) -> Vector:  # type: ignore
        incoming_light = self.sky

        hit_info = ray.cast(triangles, bvhs)

        if hit_info.hit:  # type: ignore
            sin = ti.abs(ti.math.dot(ray.direction, hit_info.normal))  # type: ignore
            incoming_light = sin * self.hit_color

        return incoming_light
