import os

from .spatial import Spatial


class Scene:
    def __init__(self, dir: str):
        self.spatials: list[Spatial] = []

        for root, _, files in os.walk(dir):
            for file in files:
                self.spatials.append(Spatial(root, file))
