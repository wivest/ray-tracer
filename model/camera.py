import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3


from .ray import Ray
from .hit_info import HitInfo
from .transform import Transform


COLOR = Vector((1, 1, 1), f32)
SPECULAR = 0.5


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
            diffuse = self.get_diffuse(ray, objects, 16, 5)
            specular = self.get_specular(ray, objects, 5)
            self.pixels[x, y] = diffuse * (1 - SPECULAR) + specular * SPECULAR

    @ti.func
    def get_specular(self, ray: Ray, objects: ti.template(), reflections: int) -> Vector:  # type: ignore
        hit_info = ray.cast(objects)
        ray_dir = ti.math.reflect(ray.direction, hit_info.normal)
        bounced = Ray(hit_info.point, ray_dir)
        color = self.check_miss(hit_info, ray.direction)

        while reflections > 0 and hit_info.hit:
            hit_info = bounced.cast(objects)  # type: ignore
            ray_dir = ti.math.reflect(bounced.direction, hit_info.normal)  # type: ignore
            color = color * self.check_miss(hit_info, bounced.direction)  # type: ignore
            bounced = Ray(hit_info.point, ray_dir)
            reflections -= 1

        return color

    @ti.func
    def get_diffuse(self, ray: Ray, objects: ti.template(), samples: int, reflections: int) -> Vector:  # type: ignore
        accumulated = vec3(0)

        for _ in range(samples):
            refl_iter = reflections

            hit_info = ray.cast(objects)
            ray_dir = self.random_hemisphere(hit_info.normal)
            bounced = Ray(hit_info.point, ray_dir)
            color = self.check_miss(hit_info, ray.direction)

            while refl_iter > 0 and hit_info.hit:
                hit_info = bounced.cast(objects)  # type: ignore
                ray_dir = self.random_hemisphere(hit_info.normal)
                color = color * self.check_miss(hit_info, bounced.direction)  # type: ignore
                bounced = Ray(hit_info.point, ray_dir)

                refl_iter -= 1

            accumulated += color

        return accumulated / samples

    @ti.func
    def random_hemisphere(self, normal: vec3) -> Vector:  # type: ignore
        x = ti.randn()
        y = ti.randn()
        z = ti.randn()
        dir = vec3(x, y, z)
        if ti.math.dot(dir, normal) < 0:
            dir *= -1
        return dir.normalized()

    @ti.func
    def check_miss(self, hit_info: HitInfo, direction: vec3) -> Vector:  # type: ignore
        color = hit_info.color
        if not hit_info.hit:
            color = self.sky(direction)
        return color

    @ti.func
    def sky(self, direction: vec3) -> Vector:  # type: ignore
        return COLOR * direction

    @ti.func
    def is_shadow(self, point: vec3, light: vec3, objects: ti.template()) -> bool:  # type: ignore
        ray = Ray(point, (light - point).normalized())  # type: ignore
        return ray.cast(objects).hit  # type: ignore
