from imports.common import *

from pygltflib import GLTF2

from .transform import Transform
from .lenses import Lens


TRANSLATION_NONE = [0.0, 0.0, 0.0]
ROTATION_NONE = [0.0, 0.0, 0.0, 0.0]
PERSPECTIVE_NONE = 0.4


@ti.data_oriented
class Camera:

    lens: Lens

    def __init__(
        self,
        size: tuple[int, int],
        transform: Transform,
    ):
        self.transform = transform
        self.size = size
        self.pixels = Vector.field(3, f32, self.size)

    @staticmethod
    def list_transforms(gltf: GLTF2):
        scene = gltf.scenes[gltf.scene]
        if scene.nodes == None:
            raise Exception()

        for i in scene.nodes:
            node = gltf.nodes[i]
            if node.camera != None:
                t = node.translation or TRANSLATION_NONE
                r = node.rotation or ROTATION_NONE
                p = gltf.cameras[node.camera].perspective
                angle = p.yfov if p else PERSPECTIVE_NONE

                origin, bas = Transform.convert_transform(t, r)
                yield Transform(origin, bas, angle)

    def render(self, triangles: StructField, bvhs: StructField) -> bool:
        return self.lens.render(self.pixels, triangles, bvhs)
