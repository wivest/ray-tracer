import taichi as ti

COLOR: ti.Vector = ti.Vector((1.0, 0.0, 0.0), ti.f32)


@ti.data_oriented
class Camera:
    pixels: ti.MatrixField

    def __init__(self, size: tuple[int, int]):
        self.pixels = ti.Vector.field(3, ti.f32, size)

    @ti.kernel
    def render(self):
        for x, y in self.pixels:
            self.pixels[x, y] = COLOR
