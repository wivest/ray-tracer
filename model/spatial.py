import struct
import numpy as np
from numpy import ndarray
from pygltflib import GLTF2, Node, Mesh, Primitive
from scipy.spatial.transform import Rotation


from imports.common import *
from imports.aliases import vec

from .py_material import PyMaterial


@ti.data_oriented
class Spatial:

    BVH_DEPTH: int = 1

    def __init__(self, mesh: Mesh, node: Node, gltf: GLTF2):
        self.__init_dict(mesh, gltf)

        offset = 0
        for primitive in mesh.primitives:
            offset += self.__parse(primitive, node, gltf, offset)

        self.__calculate_BVHs()

    def __init_dict(self, mesh: Mesh, gltf: GLTF2):
        self.n = 0
        for primitive in mesh.primitives:
            if primitive.indices == None:
                continue
            accessor = gltf.accessors[primitive.indices]
            self.n += accessor.count // 3

        self.materials = {
            "diffuse": np.empty(shape=(self.n, 3), dtype=np.float32),
            "specular": np.empty(shape=(self.n, 3), dtype=np.float32),
            "emission": np.empty(shape=(self.n, 3), dtype=np.float32),
        }
        self.triangles = {
            "a": np.empty(shape=(self.n, 3), dtype=np.float32),
            "b": np.empty(shape=(self.n, 3), dtype=np.float32),
            "c": np.empty(shape=(self.n, 3), dtype=np.float32),
            "normal": np.empty(shape=(self.n, 3), dtype=np.float32),
        }

    def __parse(
        self, primitive: Primitive, node: Node, gltf: GLTF2, offset: int
    ) -> int:
        vertices: list[vec] = list(self.__get_vertices(primitive, node, gltf))
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
            self.__assign_triangle(offset + i, a, b, c, material)
        return len(tris)

    def __assign_triangle(self, i: int, a: vec, b: vec, c: vec, mtl: PyMaterial):
        self.triangles["a"][i] = a
        self.triangles["b"][i] = b
        self.triangles["c"][i] = c
        for key in mtl:
            self.materials[key][i] = mtl[key]

    def __get_vertices(self, primitive: Primitive, node: Node, gltf: GLTF2):
        scale = node.scale or [1, 1, 1]
        r = node.rotation or [0, 0, 0, 1]
        rotation = Rotation.from_quat(r)
        translation = node.translation or [0, 0, 0]

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
            x, y, z = struct.unpack("fff", data[idx : idx + 12])
            yield Spatial.__apply_transform((x, y, z), scale, rotation, translation)

    @staticmethod
    def __apply_transform(
        point: vec, scale: list[float], rotation: Rotation, translation: list[float]
    ) -> vec:
        x = point[0] * scale[0]
        y = point[1] * scale[1]
        z = point[2] * scale[2]
        v: list[float] = rotation.apply(np.array((x, y, z))).tolist()  # type: ignore
        x, y, z = v
        x += translation[0]
        y += translation[1]
        z += translation[2]
        return (x, y, z)

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

    def __calculate_BVHs(self):
        depth: int = 2**self.BVH_DEPTH - 1
        self.aabbs = {
            "min_point": np.empty(shape=(depth, 3), dtype=np.float32),
            "max_point": np.empty(shape=(depth, 3), dtype=np.float32),
        }
        self.bvhs = {
            "first": np.empty(shape=depth, dtype=np.int32),
            "second": np.empty(shape=depth, dtype=np.int32),
            "start": np.empty(shape=depth, dtype=np.int32),
            "length": np.empty(shape=depth, dtype=np.int32),
        }

        self.__update_BVH(0, 0)

    def __update_BVH(self, idx: int, depth: int):
        if depth == self.BVH_DEPTH:
            self.bvhs["first"][(idx - 1) // 2] = 0
            self.bvhs["second"][(idx - 1) // 2] = 0
            return

        min_point, max_point = self.__get_AABB(0, self.n)

        self.aabbs["min_point"][idx] = min_point
        self.aabbs["max_point"][idx] = max_point
        self.bvhs["first"][idx] = 0
        self.bvhs["second"][idx] = 0
        self.bvhs["start"][idx] = 0
        self.bvhs["length"][idx] = 0 + self.n

        self.__update_BVH(2 * idx + 1, depth + 1)
        self.__update_BVH(2 * idx + 2, depth + 1)
        self.__sort_triangles(0, self.n, idx)

    def __sort_triangles(self, start: int, count: int, idx: int) -> int:
        min_point = self.aabbs["min_point"][idx]
        max_point = self.aabbs["max_point"][idx]

        sides = max_point - min_point
        aabb_center = (max_point + min_point) / 2
        split = np.argmax(sides)
        second = start

        for i in range(start, start + count):
            center = (
                self.triangles["a"][i] + self.triangles["b"][i] + self.triangles["c"][i]
            ) / 3
            if center[split] < aabb_center[split]:
                self.__swap_triangles(i, second)
                second += 1
        print("indices: ", start, count, second, "\nsplit: ", split, aabb_center, sides)
        self.__get_AABB(start, second - start)
        self.__get_AABB(second, start + count - second)

        return second

    def __swap_triangles(self, a: int, b: int):
        if a == b:
            return
        for arr in self.materials.values():
            arr[a], arr[b] = arr[b], arr[a]
        for arr in self.triangles.values():
            arr[[a, b]] = arr[[b, a]]

    def __get_AABB(self, start: int, count: int) -> tuple[ndarray, ndarray]:
        points = np.concatenate(
            [
                self.triangles["a"][start : start + count],
                self.triangles["b"][start : start + count],
                self.triangles["c"][start : start + count],
            ]
        )
        min_point = np.amin(points, axis=0)
        max_point = np.amax(points, axis=0)
        print(min_point, max_point)

        return min_point, max_point

    @ti.kernel
    def _update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
