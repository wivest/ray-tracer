from pygltflib import GLTF2
from scipy.spatial.transform import Rotation

from imports.common import *
from imports.aliases import vec, basis


class Transform:

    def __init__(
        self, origin: vec, transform_basis: basis, angle: float, ratio: float | None
    ):
        ORIG = Vector(origin, f32)
        self.origin = Vector.field(3, f32, ())
        self.origin[None] = ORIG

        MAT = Matrix(transform_basis, f32)
        self.basis = Matrix.field(3, 3, f32, ())
        self.basis[None] = MAT

        self.angle = angle
        self.ratio = ratio

    @classmethod
    def from_gltf(cls, path: str):
        data = GLTF2().load(path)
        if data == None:
            raise Exception()
        scene = data.scenes[data.scene]
        if scene.nodes == None:
            raise Exception()

        t = []
        r = []
        angle = 0.4
        ratio: float | None = None
        for i in scene.nodes:
            node = data.nodes[i]
            if node.camera != None:
                t = node.translation
                r = node.rotation
                p = data.cameras[node.camera].perspective
                if p != None:
                    angle = p.yfov
                    ratio = p.aspectRatio

        if t == None or r == None:
            raise Exception()

        origin, bas = Transform.__convert_transform(t, r)
        return cls(origin, bas, angle, ratio)

    @staticmethod
    def __convert_transform(translation: list[float], rotation: list[float]):
        origin = (translation[0], translation[1], translation[2])
        mat = Rotation.from_quat(rotation).as_matrix()
        bas: basis = tuple(tuple(i) for i in mat.tolist())  # type: ignore

        return origin, bas

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
