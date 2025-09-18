from imports.common import *

from pygltflib import GLTF2

from .transform import Transform, NONE_DATA
from .lenses import Lens, Preview, Render


@ti.data_oriented
class Camera:

    def __init__(self, size: tuple[int, int], transform: Transform):
        self.transform = transform
        self.size = size
        self.pixels = Vector.field(3, f32, self.size)

        self.preview_lens = Preview(size, transform)
        self.render_lens = Render(size, transform, 64)
        self.lens: Lens = self.preview_lens

    @staticmethod
    def list_transforms(gltf: GLTF2):
        scene = gltf.scenes[gltf.scene]
        if scene.nodes == None:
            raise Exception()

        for i in scene.nodes:
            node = gltf.nodes[i]
            if node.camera != None:
                t = node.translation or NONE_DATA[0]
                r = node.rotation or NONE_DATA[1]
                p = gltf.cameras[node.camera].perspective
                angle = p.yfov if p else NONE_DATA[2]

                origin, bas = Transform.convert_transform(t, r)
                yield Transform(origin, bas, angle)

    def render(
        self, triangles: StructField, bvhs: StructField, lights: StructField
    ) -> bool:
        return self.lens.render(self.pixels, triangles, bvhs, lights)
