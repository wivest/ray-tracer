from imports.common import *

from .transform import Transform
from .lenses.preview import Preview


@ti.data_oriented
class Camera:

    def __init__(
        self,
        size: tuple[int, int],
        gltf_path: str,
        angle: float,
    ):
        self.transform = Transform.get_camera_data(gltf_path)
        self.pixels = Vector.field(3, f32, size)
        self.fov: float = size[1] / ti.tan(angle / 2)

        self.lens = Preview(size, gltf_path, angle)

    def render(self, objects: StructField):
        self.lens.render(self.pixels, objects)
