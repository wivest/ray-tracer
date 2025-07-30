import numpy as np
from pygltflib import GLTF2

from imports.common import *

from .spatial import Spatial
from .triangle import Triangle


@ti.data_oriented
class Scene:

    def __init__(self, path: str):
        gltf = GLTF2().load(path)
        if gltf == None:
            raise Exception()

        self.spatials: list[Spatial] = []
        nodes = gltf.scenes[gltf.scene].nodes or []
        for i in nodes:
            node = gltf.nodes[i]
            if node.mesh == None:
                continue
            mesh = gltf.meshes[node.mesh]
            self.spatials.append(Spatial(mesh, node, gltf))

    def export(self) -> StructField:
        n = 0
        materials = {}
        triangles = {}

        for spatial in self.spatials:
            n += spatial.n

        for key in ["diffuse", "specular", "emission"]:
            materials[key] = np.concatenate(
                [s.materials[key] for s in self.spatials], dtype=np.float32
            )
        triangles["material"] = materials
        for key in ["a", "b", "c", "normal"]:
            triangles[key] = np.concatenate(
                [s.triangles[key] for s in self.spatials], dtype=np.float32
            )

        f = Triangle.field(shape=n)
        f.from_numpy(triangles)
        self._update_normals(f)
        return f

    @ti.kernel
    def _update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
