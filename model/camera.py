from imports.common import *

from . import tonemapping
from .transform import Transform
from .ray import Ray
from .hit_info import HitInfo

# from light.point import Point
from light.sun import Sun
from sky.colored import Colored


@ti.data_oriented
class Camera:

    def __init__(self, size: tuple[int, int], angle: float, samples: int):
        self.transform = Transform()
        self.pixels = Vector.field(3, f32, size)
        self.fov: float = size[1] / ti.tan(angle / 2)
        self.sky = Colored(Vector((1.0, 1.0, 1.0)))
        self.samples = samples

        self._sampled = Vector.field(3, f32, size)
        self._sampled.fill(0.0)
        self._ready: Field = ti.field(int, ())
        self._ready[None] = 0

    @ti.kernel
    def reset_samples(self):
        self._sampled.fill(0.0)
        self._ready[None] = 0

    @ti.kernel
    def render(self, objects: ti.template()):  # type: ignore
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        self._ready[None] += 1

        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = self.transform.basis[None] @ pixel
            ray = Ray(self.transform.origin[None], direction)

            incoming_light = self.get_color(ray, objects, 6)
            self._sampled[x, y] += tonemapping.aces(incoming_light)
            self.pixels[x, y] = self._sampled[x, y] / self._ready[None]

    @ti.func
    def get_color(self, ray: Ray, objects: ti.template(), hits: int) -> Vector:  # type: ignore
        light = Sun(Vector((1.5, 1.5, 1.5)), Vector((-1, -1, -1)))
        incoming_light = Vector((0.0, 0.0, 0.0))
        ray_color = Vector((1.0, 1.0, 1.0))

        for i in range(hits):
            hit_info = ray.cast(objects)
            if not hit_info.hit:
                incoming_light += ray_color * self.sky.get(ray.direction)  # type: ignore
                break

            ray = self._bounce_ray(ray, hit_info)
            sin = ti.math.dot(ray.direction, hit_info.normal)
            ray_color = sin * ray_color * hit_info.material.diffuse
            incoming_light += ray_color * (
                hit_info.material.emmision
                + self.sample_direct_light(hit_info.point, objects, light)
            )

        return incoming_light

    @ti.func
    def _bounce_ray(self, ray: Ray, hit_info: HitInfo) -> Ray:  # type: ignore
        specular = ti.math.reflect(ray.direction, hit_info.normal)
        diffuse = self._random_hemisphere(hit_info.normal)
        ray_dir = ti.math.mix(
            diffuse, specular, hit_info.material.specular
        ).normalized()
        return Ray(hit_info.point, ray_dir)

    @ti.func
    def _random_hemisphere(self, normal: vec3) -> Vector:  # type: ignore
        x = ti.randn()
        y = ti.randn()
        z = ti.randn()
        dir = vec3(x, y, z)
        if ti.math.dot(dir, normal) < 0:
            dir *= -1
        return dir.normalized()

    @ti.func
    def sample_direct_light(self, point: vec3, objects: ti.template(), light: ti.template()) -> Vector:  # type: ignore
        sampled = Vector((0.0, 0.0, 0.0))

        if light.is_visible(point, objects):
            sampled = light.color

        return sampled
