from taichi import StructField, Vector

from model.triangle import Triangle
from model.material import Material


class Spatial:

    def __init__(self, path: str):
        self.faces: list[
            tuple[
                tuple[float, float, float],
                tuple[float, float, float],
                tuple[float, float, float],
                Material,  # type: ignore
            ]
        ] = []

        with open(path) as file:
            self.__parse(file.readlines())

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

        with open(path) as file:
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
                    current.color = (r, g, b)  # type: ignore
                elif key == "Ks":
                    current.specular = float(tokens[1])  # type: ignore

        return materials

    def export(self) -> StructField:
        n = len(self.faces)
        data = Triangle.field(shape=n)

        for i in range(n):
            face = self.faces[i]
            data[i] = Triangle(
                Vector(face[0]), Vector(face[1]), Vector(face[2]), face[3]
            )

        return data
