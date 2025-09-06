from imports.common import *

from .transform import Transform
from .lenses import Lens


@ti.data_oriented
class Camera:

    lens: Lens

    def __init__(
        self,
        size: tuple[int, int],
        gltf_path: str,
    ):
        self.transform = Transform.from_gltf(gltf_path)
        size = (int(size[1] * self.transform.ratio), size[1])
        self.pixels = Vector.field(3, f32, size)

    def render(self, triangles: StructField, bvhs: StructField):
        self.lens.render(self.pixels, triangles, bvhs)
