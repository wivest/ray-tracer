import struct
import numpy as np
from pygltflib import GLTF2, Mesh, Primitive

from imports.common import *
from imports.aliases import vec

from .triangle import Triangle
from .py_material import PyMaterial


@ti.data_oriented
class Spatial:

    def __init__(self, mesh: Mesh, gltf: GLTF2):
        self.__init_dict(mesh, gltf)

        for primitive in mesh.primitives:
            self.__parse(primitive, gltf)

    def __init_dict(self, mesh: Mesh, gltf: GLTF2):
        self.n = 0
        for primitive in mesh.primitives:
            accessor = gltf.accessors[primitive.attributes.POSITION or 0]
            self.n += accessor.count

        self.materials = {
            "diffuse": np.empty(shape=(self.n, 3), dtype=np.float32),
            "specular": np.empty(shape=(self.n, 3), dtype=np.float32),
            "emission": np.empty(shape=(self.n, 3), dtype=np.float32),
        }
        self.triangles = {
            "a": np.empty(shape=(self.n, 3), dtype=np.float32),
            "b": np.empty(shape=(self.n, 3), dtype=np.float32),
            "c": np.empty(shape=(self.n, 3), dtype=np.float32),
            "material": self.materials,
            "normal": np.empty(shape=(self.n, 3), dtype=np.float32),
        }

    def __parse(self, primitive: Primitive, gltf: GLTF2):
        vertices: list[vec] = list(self.__get_triangles(primitive, gltf))
        tris = list(self.__get_indices(primitive, gltf))
        material = (
            PyMaterial(gltf.materials[primitive.material])
            if primitive.material != None
            else PyMaterial()
        )

        for i in range(len(tris)):
            a = vertices[tris[i][0]]
            b = vertices[tris[i][1]]
            c = vertices[tris[i][2]]
            self.__assign_triangle(i, a, b, c, material)

    def __assign_triangle(self, i: int, a: vec, b: vec, c: vec, mtl: PyMaterial):
        self.triangles["a"][i] = a
        self.triangles["b"][i] = b
        self.triangles["c"][i] = c
        for key in mtl:
            self.materials[key][i] = mtl[key]

    def __get_triangles(self, primitive: Primitive, gltf: GLTF2):
        accessor = gltf.accessors[primitive.attributes.POSITION or 0]
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
            yield (a, b, c)

    def __get_indices(self, primitive: Primitive, gltf: GLTF2):
        accessor = gltf.accessors[primitive.indices or 0]  # type: ignore
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
