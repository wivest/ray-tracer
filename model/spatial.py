import numpy as np

from imports.common import *

from .triangle import Triangle
from .material import Material


@ti.data_oriented
class Spatial:

    def __init__(self, scene: str, path: str):
        self.scene_path = scene
        self.faces: list[
            tuple[
                tuple[float, float, float],
                tuple[float, float, float],
                tuple[float, float, float],
                Material,  # type: ignore
            ]
        ] = []

        with open(self.scene_path + path) as file:
            lines = file.readlines()

            n = self.__count_triangles(lines)
            self.tmp_materials = {
                "diffuse": np.empty(shape=(n, 3), dtype=np.float32),
                "specular": np.empty(shape=(n, 3), dtype=np.float32),
                "emmision": np.empty(shape=(n, 3), dtype=np.float32),
            }
            self.tmp_triangles = {
                "a": np.empty(shape=(n, 3), dtype=np.float32),
                "b": np.empty(shape=(n, 3), dtype=np.float32),
                "c": np.empty(shape=(n, 3), dtype=np.float32),
                "material": self.tmp_materials,
                "normal": np.empty(shape=(n, 3), dtype=np.float32),
            }

            self.__parse(lines)

        self.triangles = Triangle.field(shape=n)
        self._export()
        self._update_normals()

    def __parse(self, lines: list[str]):
        vertices: list[tuple[float, float, float]] = []
        materials: dict[str, Material] = {}  # type: ignore
        current = Material()

        def vertex_i(tokens: list[str], i: int) -> int:
            return int(tokens[i].split("/")[0]) - 1

        for line in lines:
            tokens = line.split()
            key = tokens[0]

            if key == "v":
                x = float(tokens[1])
                y = float(tokens[2])
                z = float(tokens[3])
                vertices.append((x, y, z))
            elif key == "f":
                a = vertices[vertex_i(tokens, 1)]
                b = vertices[vertex_i(tokens, 2)]
                c = vertices[vertex_i(tokens, 3)]
                self.faces.append((a, b, c, current))
            elif key == "mtllib":
                new_materials = self.__load_materials(tokens[1])
                materials.update(new_materials)
            elif key == "usemtl":
                current = materials[tokens[1]]

    def __load_materials(self, path: str) -> dict[str, Material]:  # type: ignore
        materials: dict[str, Material] = {}  # type: ignore

        with open(self.scene_path + path) as file:
            lines = file.readlines()
            current = Material()

            for line in lines:
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                key = tokens[0]

                if key == "newmtl":
                    current = Material()
                    materials[tokens[1]] = current
                elif key == "Kd":
                    r = float(tokens[1])
                    g = float(tokens[2])
                    b = float(tokens[3])
                    current.diffuse = (r, g, b)  # type: ignore
                elif key == "Ks":
                    r = float(tokens[1])
                    g = float(tokens[2])
                    b = float(tokens[3])
                    current.specular = (r, g, b)  # type: ignore
                elif key == "Ke":
                    r = float(tokens[1])
                    g = float(tokens[2])
                    b = float(tokens[3])
                    current.emission = (r, g, b)  # type: ignore

        return materials

    def __count_triangles(self, lines: list[str]) -> int:
        count = 0

        for line in lines:
            if line[0:2] == "f ":
                count += 1

        return count

    def _export(self):
        for i in range(len(self.faces)):
            face = self.faces[i]
            self.triangles[i] = Triangle(
                Vector(face[0]), Vector(face[1]), Vector(face[2]), face[3]
            )

    @ti.kernel
    def _update_normals(self):
        for i in self.triangles:
            self.triangles[i].update_normal()  # type: ignore
