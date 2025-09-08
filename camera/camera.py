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
        r = self.transform.ratio
        self.size = (int(size[1] * r), size[1]) if r else size
        self.pixels = Vector.field(3, f32, self.size)

    def render(self, triangles: StructField, bvhs: StructField):
        self.lens.render(self.pixels, triangles, bvhs)
