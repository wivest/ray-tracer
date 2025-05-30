import os
import numpy as np

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
