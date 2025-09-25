from imports.common import *

from .lens import Lens
from ..transform import Transform
from ..ray import Ray
from ..hit_info import HitInfo


@ti.data_oriented
class Render(Lens):

    samples: int
    hits: int
    sky: Vector

    def __init__(self, size: tuple[int, int], transform: Transform):
        self.fov: float = size[1] / ti.tan(transform.angle)
        self.transform = transform

        self._sampled = Vector.field(3, f32, size)
        self._ready: Field = ti.field(int, ())
        self.reset_samples()

    def render(
        self,
        pixels: MatrixField,
        triangles: StructField,
        bvhs: StructField,
        lights: StructField,
    ) -> bool:
        if self._ready[None] < self.samples:
            self._render_sample(self._sampled, triangles, bvhs, lights)
            self._apply_sample(pixels)
            return False
        return True

    @ti.kernel
    def reset_samples(self):
        self._sampled.fill(0.0)
        self._ready[None] = 0

    @ti.kernel
    def _apply_sample(self, pixels: ti.template()):  # type: ignore
        ready = self._ready[None]
        fac = 1 / (ready + 1)
        old = ready * fac
        self._ready[None] += 1

        for x, y in pixels:
            pixels[x, y] = pixels[x, y] * old + self._sampled[x, y] * fac

    @ti.func
    def _get_color(self, ray: Ray, triangles: ti.template(), bvhs: ti.template(), lights: ti.template()) -> Vector:  # type: ignore
        incoming_light = Vector((0.0, 0.0, 0.0))
        ray_color = Vector((1.0, 1.0, 1.0))

        for _ in range(self.hits):
            hit_info = ray.cast(triangles, bvhs)
            if not hit_info.hit:
                incoming_light += ray_color * self.sky
                break

            ray = self._bounce_ray(ray, hit_info)
            sin = ti.math.dot(ray.direction, hit_info.normal)
            ray_color = sin * ray_color * hit_info.material.diffuse
            incoming_light += ray_color * (
                hit_info.material.emission
                + self._sample_direct_light(
                    hit_info.point, hit_info.normal, triangles, bvhs, lights
                )
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
    def _sample_direct_light(self, point: vec3, normal: vec3, triangles: ti.template(), bvhs: ti.template(), lights: ti.template()) -> Vector:  # type: ignore
        visible = Vector((0.0, 0.0, 0.0))

        for i in range(lights.shape[0]):
            light = lights[i]
            visible += light.sample_light(point, normal, triangles, bvhs)

        return visible
