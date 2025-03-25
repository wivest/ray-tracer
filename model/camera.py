import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

from .ray import Ray
from .transform import Transform


COLOR = Vector((1.0, 1.0, 1.0), f32)


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
            self.pixels[x, y] = self.cast_ray(ray, objects)

    @ti.func
    def cast_ray(self, ray: Ray, objects: ti.template()) -> Vector:  # type: ignore
        color = self.sky(ray.direction)
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(ray)
            if coef > 0:
                hit = ray.origin + ray.direction * coef
                normal = objects[i].normal(hit)
                reflection = ti.math.reflect(ray.direction, normal)
                color = self.sky(reflection)
        return color

    @ti.func
    def sky(self, direction: vec3) -> Vector:  # type: ignore
        return COLOR * direction
