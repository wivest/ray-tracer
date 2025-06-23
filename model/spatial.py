import os
import struct
import numpy as np
from pygltflib import GLTF2

from imports.common import *
from imports.aliases import vec

from .triangle import Triangle


class PyMaterial(dict[str, vec]):
    def assign_color(self, color: str, rgb: list[str]):
        r = float(rgb[0])
        g = float(rgb[1])
        b = float(rgb[2])
        self[color] = (r, g, b)


@ti.data_oriented
class Spatial:

    def __init__(self, path: str, gltf_path: str):
        self.scene_path = os.path.dirname(path) + "/"
        gltf = GLTF2().load(gltf_path)
        if gltf == None:
            raise Exception()
        primitives = gltf.meshes[0].primitives
        accessor = gltf.accessors[primitives[0].attributes.POSITION or 0]

        with open(path) as file:
            lines = file.readlines()

            self.n = accessor.count
            self.materials = {
                "diffuse": np.empty(shape=(self.n, 3), dtype=np.float32),
                "specular": np.empty(shape=(self.n, 3), dtype=np.float32),
                "emmision": np.empty(shape=(self.n, 3), dtype=np.float32),
            }
            self.triangles = {
                "a": np.empty(shape=(self.n, 3), dtype=np.float32),
                "b": np.empty(shape=(self.n, 3), dtype=np.float32),
                "c": np.empty(shape=(self.n, 3), dtype=np.float32),
                "material": self.materials,
                "normal": np.empty(shape=(self.n, 3), dtype=np.float32),
            }

            self.__parse(lines, gltf)

    def __parse(self, lines: list[str], gltf: GLTF2):
        vertices: list[vec] = list(self.__get_triangles_tmp(gltf))
        tris = self.__get_indices_tmp(gltf)
        mtls: dict[str, PyMaterial] = {}
        current_mtl = PyMaterial()
        tri_idx = 0

        for line in lines:
            tokens = line.split()
            key = tokens[0]

            if key == "mtllib":
                with open(self.scene_path + tokens[1]) as f:
                    mtl_lines = f.readlines()
                mtls.update(self.__load_materials(mtl_lines))

            elif key == "usemtl":
                current_mtl = mtls[tokens[1]]

        tri_idx = 0
        for tri in tris:
            a = vertices[tri[0]]
            b = vertices[tri[1]]
            c = vertices[tri[2]]
            self.__assign_triangle(tri_idx, a, b, c, current_mtl)
            tri_idx += 1

    def __assign_triangle(self, i: int, a: vec, b: vec, c: vec, mtl: PyMaterial):
        self.triangles["a"][i] = a
        self.triangles["b"][i] = b
        self.triangles["c"][i] = c
        for key in mtl:
            self.materials[key][i] = mtl[key]

    def __load_materials(self, lines: list[str]) -> dict[str, PyMaterial]:
        materials: dict[str, PyMaterial] = {}
        current_mtl = PyMaterial()

        for line in lines:
            tokens = line.split()
            if len(tokens) == 0:
                continue

            key = tokens[0]
            if key == "newmtl":
                current_mtl = PyMaterial()
                materials[tokens[1]] = current_mtl
            elif key == "Kd":
                current_mtl.assign_color("diffuse", tokens[1:4])
            elif key == "Ks":
                current_mtl.assign_color("specular", tokens[1:4])
            elif key == "Ke":
                current_mtl.assign_color("emmision", tokens[1:4])

        return materials

    def __get_triangles_tmp(self, gltf: GLTF2):
        primitives = gltf.meshes[0].primitives

        accessor = gltf.accessors[primitives[0].attributes.POSITION or 0]
        bufferView = gltf.bufferViews[accessor.bufferView or 0]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)

        if type(data) is not bytes:
            raise Exception()
        if bufferView.byteOffset == None:
            raise Exception()
        TYPE_SIZE = 12  # accessor.type = "VEC3"
        for i in range(accessor.count):
            idx = bufferView.byteOffset + i * TYPE_SIZE
            a, b, c = struct.unpack("fff", data[idx : idx + 12])
            yield a, b, c

    def __get_indices_tmp(self, gltf: GLTF2):
        primitives = gltf.meshes[0].primitives

        accessor = gltf.accessors[primitives[0].indices or 0]  # type: ignore
        bufferView = gltf.bufferViews[accessor.bufferView or 0]  # type: ignore
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)

        if type(data) is not bytes:
            raise Exception()
        if bufferView.byteOffset == None:
            raise Exception()
        TYPE_SIZE = 2  # accessor.type = "SCALAR"
        for i in range(accessor.count // 3):
            idx = bufferView.byteOffset + i * TYPE_SIZE * 3
            ns = struct.unpack("HHH", data[idx : idx + TYPE_SIZE * 3])
            yield ns

    def export(self) -> StructField:
        tri_field = Triangle.field(shape=self.n)
        tri_field.from_numpy(self.triangles)
        self._update_normals(tri_field)
        return tri_field

    @ti.kernel
    def _update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
