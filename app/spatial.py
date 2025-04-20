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
            ]
        ] = []

        with open(path) as file:
            self.__parse(file.readlines())

    def __parse(self, lines: list[str]):
        vertices: list[tuple[float, float, float]] = []

        def vertex_i(tokens: list[str], i: int) -> int:
            return int(tokens[i].split("/")[0]) - 1

        for line in lines:
            tokens = line.split()
            if tokens[0] == "v":
                x = float(tokens[1])
                y = float(tokens[2])
                z = float(tokens[3])
                vertices.append((x, y, z))
            elif tokens[0] == "f":
                a = vertices[vertex_i(tokens, 1)]
                b = vertices[vertex_i(tokens, 2)]
                c = vertices[vertex_i(tokens, 3)]
                self.faces.append((a, b, c))

    def export(self) -> StructField:
        n = len(self.faces)
        data = Triangle.field(shape=n)

        for i in range(n):
            face = self.faces[i]
            data[i] = Triangle(
                Vector(face[0]),
                Vector(face[1]),
                Vector(face[2]),
                Material(Vector((1, 1, 1)), 0.5, 0.5),
            )

        return data
