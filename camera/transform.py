from imports.common import *
from imports.aliases import vec, basis


class Transform:

    def __init__(self, origin: vec, transform_basis: basis):
        ORIG = Vector(origin, f32)
        self.origin = Vector.field(3, f32, ())
        self.origin[None] = ORIG

        MAT = Matrix(transform_basis, f32)
        self.basis = Matrix.field(3, 3, f32, ())
        self.basis[None] = MAT

    def rotate_local_x(self, rad: float):
        sin = ti.sin(rad)
        cos = ti.cos(rad)
        MAT = ((1, 0, 0), (0, cos, -sin), (0, sin, cos))
        rot = Matrix(MAT, f32)

        self.basis[None] = self.basis[None] @ rot

    def rotate_y(self, rad: float):
        sin = ti.sin(rad)
        cos = ti.cos(rad)
        MAT = ((cos, 0, sin), (0, 1, 0), (-sin, 0, cos))
        rot = Matrix(MAT, f32)

        self.basis[None] = rot @ self.basis[None]

    def move_x(self, by: float):
        mat = self.basis[None]
        x_axis = Vector((mat[0, 0], mat[1, 0], mat[2, 0]), f32)
        self.origin[None] += x_axis * by

    def move_y(self, by: float):
        mat = self.basis[None]
        y_axis = Vector((mat[0, 1], mat[1, 1], mat[2, 1]), f32)
        self.origin[None] += y_axis * by

    def move_z(self, by: float):
        mat = self.basis[None]
        z_axis = Vector((mat[0, 2], mat[1, 2], mat[2, 2]), f32)
        self.origin[None] += z_axis * by

    def move_flat_x(self, by: float):
        mat = self.basis[None]
        x_axis = Vector((mat[0, 0], 0, mat[2, 0]), f32)
        if x_axis.norm_sqr() < 0.001:
            return
        x_axis = x_axis.normalized()
        self.origin[None] += x_axis * by

    def move_global_y(self, by: float):
        y_axis = Vector((0, 1, 0), f32)
        self.origin[None] += y_axis * by

    def move_flat_z(self, by: float):
        mat = self.basis[None]
        z_axis = Vector((mat[0, 2], 0, mat[2, 2]), f32)
        if z_axis.norm_sqr() < 0.001:
            return
        z_axis = z_axis.normalized()
        self.origin[None] += z_axis * by
