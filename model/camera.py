import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

from .transform import Transform


COLOR: Vector = Vector((1.0, 1.0, 1.0), f32)


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
    def render(self):
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.focal), f32)
            self.pixels[x, y] = self.sky(pixel.normalized())

    @ti.func
    def sky(self, pixel: vec3) -> Vector:  # type: ignore
        direction = self.transform.basis[None] @ pixel
        return COLOR * direction
