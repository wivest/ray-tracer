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
        self.transform = Transform.get_camera_data(gltf_path)
        self.pixels = Vector.field(3, f32, size)

    def render(self, objects: StructField):
        self.lens.render(self.pixels, objects)
