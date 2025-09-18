import numpy as np
from numpy import ndarray
from pygltflib import GLTF2

from imports.common import *

from .spatial import Spatial
from .triangle import Triangle
from .bvh import BVH, BVHBuilder

from camera.camera import Camera
from camera.transform import Transform, NONE_DATA
from light.light_union import LightUnion
from light.point import Point
from light.sun import Sun


LIGHT_EXT = "KHR_lights_punctual"


@ti.data_oriented
class Scene:

    def __init__(self, path: str, camera_size: tuple[int, int]):
        gltf = GLTF2().load(path)
        if gltf == None:
            raise Exception()

        self.__generate_mesh(gltf)
        self.__extract_lights(gltf)

        self.cameras = [Camera(camera_size, t) for t in Camera.list_transforms(gltf)]
        if len(self.cameras) == 0:
            o, b = Transform.convert_transform(NONE_DATA[0], NONE_DATA[1])
            self.cameras = [Camera(camera_size, Transform(o, b, NONE_DATA[2]))]
        self.active_cam = 0

    @property
    def camera(self):
        return self.cameras[self.active_cam]

    def __generate_mesh(self, gltf: GLTF2):
        spatials: list[Spatial] = []
        nodes = gltf.scenes[gltf.scene].nodes or []
        for i in nodes:
            node = gltf.nodes[i]
            if node.mesh == None:
                continue
            mesh = gltf.meshes[node.mesh]
            spatials.append(Spatial(mesh, node, gltf))

        material_concat = self.__concat([s.materials for s in spatials])
        triangle_concat = self.__concat([s.triangles for s in spatials])
        n = sum([s.n for s in spatials])

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
        light_data = gltf.extensions[LIGHT_EXT]["lights"]

        light_list = []
        nodes = gltf.scenes[gltf.scene].nodes or []
        for i in nodes:
            node = gltf.nodes[i]
            if not (node.extensions and LIGHT_EXT in node.extensions):
                continue

            t = node.translation or [0, 0, 0]
            r = node.rotation or [0, 0, 0, 0]
            origin, bas = Transform.convert_transform(t, r)
            ext = node.extensions[LIGHT_EXT]
            l = light_data[ext["light"]]

            union: LightUnion = LightUnion()  # type: ignore
            if l["type"] == "point":
                union.select = 0
                union.point = Point(vec3(*l["color"]), vec3(*origin))
            elif l["type"] == "directional":
                union.select = 1
                d = (-x for x in bas[2])
                union.sun = Sun(vec3(*l["color"]), vec3(*d))
            light_list.append(union)

        n = len(light_list)
        self.lights = LightUnion.field(shape=n)
        for i in range(n):
            self.lights[i] = light_list[i]
