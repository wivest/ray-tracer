import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

from .ray import Ray
from .transform import Transform


COLOR = Vector((1.0, 1.0, 1.0), f32)
BLEND = 0.25


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
            self.pixels[x, y] = self.get_color(ray, objects, 3)

    @ti.func
    def get_color(self, ray: Ray, objects: ti.template(), reflections: int) -> Vector:  # type: ignore
        reflected, blended = self.cast_ray(ray, objects)
        while reflections > 0:
            reflected, color = self.cast_ray(reflected, objects)
            blended = blended * (1 - BLEND) + color * BLEND
            reflections -= 1
        return blended

    @ti.func
    def cast_ray(self, ray: Ray, objects: ti.template()) -> (Ray, Vector):  # type: ignore
        color = self.sky(ray.direction)
        ray_origin = ray.origin
        ray_dir = ray.direction

        nearest = ti.math.inf
        for i in range(objects.shape[0]):
            coef = objects[i].intersects(ray)
            if coef > 0 and coef < nearest:
                nearest = coef

                color = objects[i].color
                ray_origin = ray.origin + ray.direction * coef
                normal = objects[i].normal(ray_origin)
                ray_dir = ti.math.reflect(ray.direction, normal)

        return (Ray(ray_origin, ray_dir), color)

    @ti.func
    def sky(self, direction: vec3) -> Vector:  # type: ignore
        return COLOR * direction
