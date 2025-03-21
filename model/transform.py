from taichi import f32, Matrix, Vector
from taichi.math import vec3, mat3


class Transform:
    origin: vec3  # type: ignore
    basis: mat3  # type: ignore

    def __init__(self):
        self.origin = Vector((0, 0, 0), f32)
        self.basis = Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)), f32)
