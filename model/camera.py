import taichi as ti
from taichi import f32, Vector
from taichi.math import vec3

COLOR: Vector = Vector((1.0, 1.0, 1.0), f32)


@ti.data_oriented
class Camera:
    pixels: ti.MatrixField
    focal: float
    h: float
    v: float

    def __init__(self, size: tuple[int, int]):
        self.pixels = Vector.field(3, f32, size)
        self.focal = 100.0
        self.h = 0.0
        self.v = 0.0

    @ti.kernel
    def render(self):
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.focal), f32)
            self.pixels[x, y] = self.sky(pixel.normalized())

    @ti.func
    def sky(self, pixel: vec3) -> Vector:  # type: ignore
        return COLOR * pixel
