import os

from imports.common import *

from .spatial import Spatial
from .triangle import Triangle


@ti.data_oriented
class Scene:
    def __init__(self, dir: str):
        self.spatials: list[Spatial] = []

        for root, _, files in os.walk(dir):
            for file in files:
                if not file.endswith(".obj"):
                    continue
                self.spatials.append(Spatial(root, file))

    def export(self) -> StructField:
        n = 0
        for spatial in self.spatials:
            n += spatial.deprecated_triangles.shape[0]

        triangles = Triangle.field(shape=n)

        i = 0
        for spatial in self.spatials:
            for t in range(spatial.deprecated_triangles.shape[0]):
                triangles[i] = spatial.deprecated_triangles[t]
                i += 1

        return triangles
