import taichi as ti
from taichi import f32, Vector, Field
from taichi.math import vec3


from . import tonemapping
from .transform import Transform
from .ray import Ray
from .hit_info import HitInfo
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

            incoming_light = self.get_color(ray, objects, 5)
            self._sampled[x, y] += tonemapping.aces(incoming_light)
            self.pixels[x, y] = self._sampled[x, y] / self._ready[None]

    @ti.func
    def get_color(self, ray: Ray, objects: ti.template(), reflections: int) -> Vector:  # type: ignore
        incoming_light = Vector((0.0, 0.0, 0.0))
        ray_color = Vector((1.0, 1.0, 1.0))

        hit_info = ray.cast(objects, self.sky, ray.direction)
        bounced = self._bounce_ray(ray, hit_info)
        ray_color = ray_color * hit_info.material.diffuse
        incoming_light += ray_color * hit_info.material.emmision

        while reflections > 0 and hit_info.hit:
            hit_info = bounced.cast(objects, self.sky, hit_info.normal)  # type: ignore
            bounced = self._bounce_ray(bounced, hit_info)
            ray_color = ray_color * hit_info.material.diffuse
            incoming_light += ray_color * hit_info.material.emmision
            reflections -= 1

        if not hit_info.hit:
            incoming_light += ray_color

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
