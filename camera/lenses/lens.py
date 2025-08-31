from abc import ABC, abstractmethod

from imports.common import *

from ..transform import Transform
from ..ray import Ray
from ..tonemapping import aces


class Lens(ABC):

    transform: Transform
    fov: float

    @abstractmethod
    def render(
        self, pixels: MatrixField, triangles: StructField, bvhs: StructField
    ): ...

    @abstractmethod
    def _get_color(self, ray: Ray, triangles: ti.template(), bvhs: ti.template()) -> Vector: ...  # type: ignore

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
