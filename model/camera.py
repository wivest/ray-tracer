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

    def __init__(self, size: tuple[int, int], angle: float, objects):
        self.transform = Transform()
        self.pixels = Vector.field(3, f32, size)
        self.focal = size[1] / ti.tan(angle / 2)

        self.objects = objects

    @ti.kernel
    def render(self):
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.focal), f32).normalized()
            direction = self.transform.basis[None] @ pixel
            ray = Ray(Vector((0, 0, 0), f32), direction)
            self.pixels[x, y] = self.cast_ray(ray)

    @ti.func
    def cast_ray(self, ray: Ray) -> Vector:  # type: ignore
        color = self.sky(ray.direction)
        for i in range(self.objects.shape[0]):
            if self.objects[i].intersects(ray):
                color = self.objects[i].color
        return color

    @ti.func
    def sky(self, direction: vec3) -> Vector:  # type: ignore
        return COLOR * direction
