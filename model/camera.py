import taichi as ti
from taichi import i32, f32, Vector
from taichi.math import vec3


from .transform import Transform
from .sky import Sky
from .ray import Ray


COLOR = Vector((1, 1, 1), f32)
SPECULAR = 0.5


@ti.data_oriented
class Camera:
    transform: Transform
    pixels: ti.MatrixField
    fov: float
    sky: Sky  # type: ignore
    samples: int

    sampled: ti.MatrixField
    ready: ti.Field

    def __init__(self, size: tuple[int, int], angle: float, samples: int):
        self.transform = Transform()
        self.pixels = Vector.field(3, f32, size)
        self.fov = size[1] / ti.tan(angle / 2)
        self.sky = Sky()
        self.samples = samples

        self.sampled = Vector.field(3, f32, size)
        self.sampled.fill(0.0)
        self.ready = ti.field(int, ())
        self.ready[None] = 0

    @ti.kernel
    def reset_samples(self):
        self.sampled.fill(0.0)
        self.ready[None] = 0

    @ti.kernel
    def render(self, objects: ti.template()):  # type: ignore
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        self.ready[None] += 1

        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = self.transform.basis[None] @ pixel
            ray = Ray(self.transform.origin[None], direction)

            diffuse = self.get_diffuse(ray, objects, 16, 5)
            specular = self.get_specular(ray, objects, 5)
            self.sampled[x, y] += diffuse * (1 - SPECULAR) + specular * SPECULAR
            self.pixels[x, y] = self.sampled[x, y] / self.ready[None]

    @ti.func
    def get_specular(self, ray: Ray, objects: ti.template(), reflections: int) -> Vector:  # type: ignore
        hit_info = ray.cast(objects, self.sky)
        ray_dir = ti.math.reflect(ray.direction, hit_info.normal)
        color = hit_info.color
        bounced = Ray(hit_info.point, ray_dir)

        while reflections > 0 and hit_info.hit:
            hit_info = bounced.cast(objects, self.sky)  # type: ignore
            ray_dir = ti.math.reflect(bounced.direction, hit_info.normal)  # type: ignore
            color = color * hit_info.color
            bounced = Ray(hit_info.point, ray_dir)
            reflections -= 1

        return color

    @ti.func
    def get_diffuse(self, ray: Ray, objects: ti.template(), samples: int, reflections: int) -> Vector:  # type: ignore
        accumulated = vec3(0)

        for _ in range(samples):
            refl_iter = reflections

            hit_info = ray.cast(objects, self.sky)
            ray_dir = self.random_hemisphere(hit_info.normal)
            bounced = Ray(hit_info.point, ray_dir)
            color = hit_info.color

            while refl_iter > 0 and hit_info.hit:
                hit_info = bounced.cast(objects, self.sky)  # type: ignore
                ray_dir = self.random_hemisphere(hit_info.normal)
                color = color * hit_info.color
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
    def is_shadow(self, point: vec3, light: vec3, objects: ti.template()) -> bool:  # type: ignore
        ray = Ray(point, (light - point).normalized())  # type: ignore
        return ray.cast(objects).hit  # type: ignore
