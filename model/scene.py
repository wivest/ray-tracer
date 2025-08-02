import numpy as np
from pygltflib import GLTF2

from imports.common import *

from .spatial import Spatial
from .triangle import Triangle
from .bvh import BVH


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

    def export(self) -> tuple[StructField, StructField]:
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

        bvh_dict = [s.export_BVH() for s in self.spatials]
        aabb_concat = {}
        for key in ["min_point", "max_point"]:
            aabb_concat[key] = np.concatenate(
                [bvh["aabb"][key] for bvh in bvh_dict],
                dtype=np.int32,  # actually dict[str, [dict[str, ndarray]]]
            )

        bvh_concat = {}
        for key in ["fisrt", "second", "start", "length"]:
            bvh_concat[key] = np.concatenate(
                [bvh[key] for bvh in bvh_dict], dtype=np.int32
            )
        bvh_concat["aabb"] = aabb_concat

        bvhs = BVH.field(shape=len(self.spatials))
        bvhs.from_numpy(bvh_concat)

        return f, bvhs

    @ti.kernel
    def _update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
