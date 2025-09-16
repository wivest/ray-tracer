import numpy as np
from numpy import ndarray
from pygltflib import GLTF2

from imports.common import *

from .spatial import Spatial
from .triangle import Triangle
from .bvh import BVH, BVHBuilder
from camera.camera import Camera


LIGHT_EXT = "KHR_lights_punctual"


@ti.data_oriented
class Scene:

    def __init__(self, path: str, camera_size: tuple[int, int]):
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

        self.__generate_mesh()
        self.camera = Camera(camera_size, path)
        self.__extract_lights(gltf)

    def __generate_mesh(self):
        material_concat = self.__concat([s.materials for s in self.spatials])
        triangle_concat = self.__concat([s.triangles for s in self.spatials])
        n = sum([s.n for s in self.spatials])

        builder = BVHBuilder(triangle_concat, material_concat, n)
        builder.build_BVHs()
        triangle_concat["material"] = material_concat  # type: ignore

        self.tris = Triangle.field(shape=n)
        self.tris.from_numpy(triangle_concat)
        self._update_normals(self.tris)

        self.bvhs = BVH.field(shape=builder.bvh_count)
        self.bvhs.from_numpy(builder.bvhs)

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

    def __extract_lights(self, gltf: GLTF2):
        if not (gltf.extensions and LIGHT_EXT in gltf.extensions):
            return
        lights = gltf.extensions[LIGHT_EXT]["lights"]
        print(lights)
