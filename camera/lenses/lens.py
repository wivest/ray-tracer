from abc import ABC, abstractmethod

from imports.common import *

from ..transform import Transform
from camera.ray import Ray
from camera.tonemapping import aces


class Lens(ABC):

    transform: Transform
    fov: float

    @abstractmethod
    def render(
        self, pixels: MatrixField, triangles: StructField, bvhs: StructField
    ): ...

    def _get_color_tmp(self, ray, triangles, bvhs): ...

    @ti.kernel
    def render_sample_tmp(self, pixels: ti.template(), triangles: ti.template(), bvhs: ti.template()):  # type: ignore
        center_x = pixels.shape[0] / 2
        center_y = pixels.shape[1] / 2
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self._get_color_tmp(ray, triangles, bvhs)
            pixels[x, y] = aces(incoming_light)
