import numpy as np
from numpy import ndarray

from imports.common import *

from .aabb import AABB


@ti.dataclass
class BVH:
    aabb: AABB  # type: ignore
    left: int
    right: int
    start: int
    count: int


class BVHBuilder:

    BVH_DEPTH: int = 8
    TRI_LIMIT: int = 4

    def __init__(self, triangles, materials, n):
        self.triangles = triangles
        self.materials = materials
        self.n = n

    def build_BVHs(self):
        self.bvh_count = 0
        tree: int = 2**self.BVH_DEPTH - 1
        self.aabbs = {
            "min_point": np.empty(shape=(tree, 3), dtype=np.float32),
            "max_point": np.empty(shape=(tree, 3), dtype=np.float32),
        }
        self.bvhs = {
            "left": np.empty(shape=tree, dtype=np.int32),
            "right": np.empty(shape=tree, dtype=np.int32),
            "start": np.empty(shape=tree, dtype=np.int32),
            "count": np.empty(shape=tree, dtype=np.int32),
        }

        self.__update_BVH(depth=1, start=0, count=self.n)
        for key in self.aabbs:
            self.aabbs[key].resize((self.bvh_count, 3))
        for key in self.bvhs:
            self.bvhs[key].resize(self.bvh_count)
        self.bvhs["aabb"] = self.aabbs  # type: ignore

    def __update_BVH(self, depth: int, start: int, count: int) -> int:
        idx = self.bvh_count
        self.bvh_count += 1
        min_point, max_point = self.__get_AABB(start, count)

        self.aabbs["min_point"][idx] = min_point
        self.aabbs["max_point"][idx] = max_point
        self.bvhs["start"][idx] = start
        self.bvhs["count"][idx] = count

        if depth == self.BVH_DEPTH or count <= self.TRI_LIMIT:
            self.bvhs["left"][idx] = 0
            self.bvhs["right"][idx] = 0
        else:
            second = self.__sort_triangles(start, count, idx)
            left = self.__update_BVH(depth + 1, start, second - start)
            right = self.__update_BVH(depth + 1, second, start + count - second)
            self.bvhs["left"][idx] = left
            self.bvhs["right"][idx] = right

        return idx

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

        return second

    def __swap_triangles(self, a: int, b: int):
        if a == b:
            return
        for arr in self.materials.values():
            arr[[a, b]] = arr[[b, a]]
        for arr in self.triangles.values():
            arr[[a, b]] = arr[[b, a]]

    def __get_AABB(self, start: int, count: int) -> tuple[ndarray, ndarray]:
        if count <= 0:
            return np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0])
        points = np.concatenate(
            [
                self.triangles["a"][start : start + count],
                self.triangles["b"][start : start + count],
                self.triangles["c"][start : start + count],
            ]
        )
        min_point = np.amin(points, axis=0)
        max_point = np.amax(points, axis=0)

        return min_point, max_point
