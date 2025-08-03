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
        n = 0
        materials = {}
        triangles = {}

        for spatial in self.spatials:
            n += spatial.n

        for key in ["diffuse", "specular", "emission"]:
            materials[key] = np.concatenate(
                [s.materials[key] for s in self.spatials], dtype=np.float32
            )

        for key in ["a", "b", "c", "normal"]:
            triangles[key] = np.concatenate(
                [s.triangles[key] for s in self.spatials], dtype=np.float32
            )
        triangles["material"] = materials

        f = Triangle.field(shape=n)
        f.from_numpy(triangles)
        self._update_normals(f)

        aabb_concat = self.__concat_dicts([s.export_BVH()[0] for s in self.spatials])
        bvh_concat = self.__concat_dicts([s.export_BVH()[1] for s in self.spatials])
        bvh_concat["aabb"] = aabb_concat  # type: ignore

        bvhs = BVH.field(shape=len(self.spatials))
        bvhs.from_numpy(bvh_concat)

        return f, bvhs

    def __concat_dicts(self, dicts: list[dict[str, ndarray]]) -> dict[str, ndarray]:
        unpacked: dict[str, list[ndarray]] = {}

        for item in dicts:
            for key in item.keys():
                unpacked[key].append(item[key])

        concatenated: dict[str, ndarray] = {}
        for key in unpacked.keys():
            concatenated[key] = np.concatenate(unpacked[key])

        return concatenated

    @ti.kernel
    def _update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
