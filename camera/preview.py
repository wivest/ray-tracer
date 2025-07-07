from imports.common import *

from .tonemapping import aces
from .transform import Transform
from .ray import Ray


@ti.data_oriented
class Preview:

    sky = vec3(0.5, 0.5, 0.5)

    def __init__(
        self,
        size: tuple[int, int],
        gltf_path: str,
        angle: float,
    ):
        self.transform = Transform.get_camera_data(gltf_path)
        self.pixels = Vector.field(3, f32, size)
        self.fov: float = size[1] / ti.tan(angle / 2)

    @ti.kernel
    def render(self, objects: ti.template()):  # type: ignore
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self.get_preview_color(ray, objects)
            self.pixels[x, y] = aces(incoming_light)

    @ti.func
    def get_preview_color(self, ray: Ray, objects: ti.template()) -> Vector:  # type: ignore
        incoming_light = self.sky

        hit_info = ray.cast(objects)
        if hit_info.hit:
            sin = ti.abs(ti.math.dot(ray.direction, hit_info.normal))
            incoming_light = sin * (
                hit_info.material.emission + hit_info.material.diffuse
            )

        return incoming_light
