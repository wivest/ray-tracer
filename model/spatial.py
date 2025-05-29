import numpy as np

from imports.common import *

from .triangle import Triangle
from .material import Material


# alias
vec = tuple[float, float, float]


class PyMaterial:
    def __init__(self):
        self.colors: dict[str, vec] = {}

    def assign_color(self, color: str, rgb: list[str]):
        r = float(rgb[0])
        g = float(rgb[1])
        b = float(rgb[2])
        self.colors[color] = (r, g, b)


@ti.data_oriented
class Spatial:

    def __init__(self, scene: str, path: str):
        self.scene_path = scene
        self.faces: list[tuple[vec, vec, vec, PyMaterial]] = []

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
        # self._export()
        # self._update_normals()

    def __parse(self, lines: list[str]):
        vertices: list[vec] = []
        materials: dict[str, PyMaterial] = {}
        current = PyMaterial()
        tri_i = 0

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
                self.__assign_triangle(tri_i, a, b, c, current)
                self.faces.append((a, b, c, current))
                tri_i += 1
            elif key == "mtllib":
                new_materials = self.__load_materials(tokens[1])
                materials.update(new_materials)
            elif key == "usemtl":
                current = materials[tokens[1]]

    def __assign_triangle(self, idx: int, a: vec, b: vec, c: vec, mtl: PyMaterial):
        self.tmp_triangles["a"][idx] = a
        self.tmp_triangles["b"][idx] = b
        self.tmp_triangles["c"][idx] = c
        for key in mtl.colors:
            self.tmp_materials[key][idx] = mtl.colors[key]

    def __load_materials(self, path: str) -> dict[str, PyMaterial]:
        materials: dict[str, PyMaterial] = {}

        with open(self.scene_path + path) as file:
            lines = file.readlines()
            current = PyMaterial()

            for line in lines:
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                key = tokens[0]

                if key == "newmtl":
                    current = PyMaterial()
                    materials[tokens[1]] = current
                elif key == "Kd":
                    current.assign_color("diffuse", tokens[1:4])
                elif key == "Ks":
                    current.assign_color("specular", tokens[1:4])
                elif key == "Ke":
                    current.assign_color("emmision", tokens[1:4])

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
                Vector(face[0]), Vector(face[1]), Vector(face[2])
            )

    def tmp_export(self) -> StructField:
        tri_field = Triangle.field(shape=len(self.faces))
        tri_field.from_numpy(self.tmp_triangles)
        self._tmp_update_normals(tri_field)
        return tri_field

    @ti.kernel
    def _update_normals(self):
        for i in self.triangles:
            self.triangles[i].update_normal()  # type: ignore

    @ti.kernel
    def _tmp_update_normals(self, triangles: ti.template()):  # type: ignore
        for i in triangles:
            triangles[i].update_normal()  # type: ignore
