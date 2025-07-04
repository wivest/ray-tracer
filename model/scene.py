import numpy as np
from pygltflib import GLTF2

from imports.common import *

from .spatial import Spatial


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
            self.spatials.append(Spatial(mesh, gltf))

    def export(self):
        n = 0
        for spatial in self.spatials:
            n += spatial.n
