import numpy as np
from numpy import ndarray
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
        material_concat = self.__concat([s.materials for s in self.spatials])
        triangle_concat = self.__concat([s.triangles for s in self.spatials])
        triangle_concat["material"] = material_concat  # type: ignore

        n = 0
        bvh_count = 0
        aabb_list = []
        bvh_list = []
        for i in range(len(self.spatials)):
            aabb_list.append(self.spatials[i].aabbs)
            bvh_list.append(self.spatials[i].bvhs)
            n += self.spatials[i].n
            bvh_count += self.spatials[i].bvh_count

        aabb_concat = self.__concat(aabb_list)
        bvh_concat = self.__concat(bvh_list)
        bvh_concat["aabb"] = aabb_concat  # type: ignore

        f = Triangle.field(shape=n)
        f.from_numpy(triangle_concat)
        self._update_normals(f)

        bvhs = BVH.field(shape=2**Spatial.BVH_DEPTH - 1)
        bvhs.from_numpy(bvh_concat)

        return f, bvhs

    def __concat(self, dicts: list[dict[str, ndarray]]) -> dict[str, ndarray]:
        unpacked: dict[str, list[ndarray]] = {}

        for item in dicts:
            for key in item.keys():
                if key not in unpacked:
                    unpacked[key] = []
                unpacked[key].append(item[key])

        concatenated: dict[str, ndarray] = {}
        for key in unpacked.keys():
            concatenated[key] = np.concatenate(unpacked[key])

        return concatenated

    @ti.kernel
    def _update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
