from imports.common import *

from .transform import Transform
from .lenses import Lens


@ti.data_oriented
class Camera:

    def __init__(
        self,
        size: tuple[int, int],
        gltf_path: str,
        lens: Lens,
    ):
        self.transform = Transform.get_camera_data(gltf_path)
        self.pixels = Vector.field(3, f32, size)

        self.lens = lens

    def render(self, objects: StructField):
        self.lens.transform = self.transform
        self.lens.render(self.pixels, objects)
