from imports.common import *

from .bvh import AABBwTriangles, BVH


class PyBVH:
    def __init__(self, triangles: StructField):
        self.triangles = triangles

    def export(self) -> BVH:  # type: ignore
        tmp = AABBwTriangles.field(shape=(1))
        return BVH(tmp, self.triangles)
