from taichi import StructField

from model.triangle import Triangle


class Spatial:

    def __init__(self, path: str):
        self.faces = []

        with open(path) as file:
            self.__parse(file.readlines())

    def __parse(self, lines: list[str]):
        vertices: list[tuple[float, float, float]] = []

        for line in lines:
            tokens = line.split()
            if tokens[0] == "v":
                x = float(tokens[1])
                y = float(tokens[2])
                z = float(tokens[3])
                vertices.append((x, y, z))
            elif tokens[0] == "f":
                print(tokens[1], tokens[2], tokens[3])

    def export(self) -> StructField:
        data = Triangle.field()
        return data
