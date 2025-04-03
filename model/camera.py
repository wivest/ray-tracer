import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

from .ray import Ray
from .hit_info import HitInfo
from .transform import Transform


COLOR = Vector((1, 1, 1), f32)
SPECULAR = 0.75


@ti.data_oriented
class Camera:
    transform: Transform
    pixels: ti.MatrixField
    focal: float

    def __init__(self, size: tuple[int, int], angle: float):
        self.transform = Transform()
        self.pixels = Vector.field(3, f32, size)
        self.focal = size[1] / ti.tan(angle / 2)

    @ti.kernel
    def render(self, objects: ti.template()):  # type: ignore
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.focal), f32).normalized()
            direction = self.transform.basis[None] @ pixel
            ray = Ray(self.transform.origin[None], direction)
            self.pixels[x, y] = self.get_color(ray, objects, 5)

    @ti.func
    def get_color(self, ray: Ray, objects: ti.template(), reflections: int) -> Vector:  # type: ignore
        LIGHT = vec3(0, 50, 0)
        hit_info = self.cast_ray(ray, objects)
        color = hit_info.color

        while reflections > 0 and hit_info.hit:
            hit_info = self.cast_ray(hit_info.reflected, objects)
            color = color * hit_info.color
            reflections -= 1
        return color

    @ti.func
    def get_diffuse(self, ray: Ray, objects: ti.template(), samples: int, reflections: int) -> Vector:  # type: ignore
        return vec3(0, 0, 0)

    @ti.func
    def random_hemisphere(self, normal: vec3) -> Vector:  # type: ignore
        x = ti.randn()
        y = ti.randn()
        z = ti.randn()
        dir = vec3(x, y, z)
        if ti.math.dot(dir, normal) < 0:
            dir *= -1
        return dir

    @ti.func
    def cast_ray(self, ray: Ray, objects: ti.template()) -> HitInfo:  # type: ignore
        color = self.sky(ray.direction)
        ray_origin = ray.origin
        ray_dir = ray.direction
        hit = False

        nearest = ti.math.inf
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(ray)
            if coef > 0 and coef < nearest:
                nearest = coef
                hit = True

                color = objects[i].color
                ray_origin = ray.origin + ray.direction * coef
                normal = objects[i].normal(ray_origin)
                ray_dir = ti.math.reflect(ray.direction, normal)

        return HitInfo(Ray(ray_origin, ray_dir), color, hit)

    @ti.func
    def sky(self, direction: vec3) -> Vector:  # type: ignore
        return COLOR * direction

    @ti.func
    def is_shadow(self, point: vec3, light: vec3, objects: ti.template()) -> bool:  # type: ignore
        ray = Ray(point, (light - point).normalized())
        return self.cast_ray(ray, objects).hit
