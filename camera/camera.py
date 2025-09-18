from imports.common import *

from pygltflib import GLTF2

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

    @staticmethod
    def list_cameras(gltf: GLTF2):
        scene = gltf.scenes[gltf.scene]
        if scene.nodes == None:
            raise Exception()

        angle = 0.4
        ratio: float | None = None
        for i in scene.nodes:
            node = gltf.nodes[i]
            if node.camera != None:
                t = node.translation or [0, 0, 0]
                r = node.rotation or [0, 0, 0, 0]
                p = gltf.cameras[node.camera].perspective
                if p != None:
                    angle = p.yfov
                    ratio = p.aspectRatio

                origin, bas = Transform.convert_transform(t, r)
                print(origin, bas, angle, ratio, sep="\n", end="\n\n")

    def render(self, triangles: StructField, bvhs: StructField) -> bool:
        return self.lens.render(self.pixels, triangles, bvhs)
