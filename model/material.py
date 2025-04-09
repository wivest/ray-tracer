import taichi as ti
from taichi import f32
from taichi.math import vec3


@ti.dataclass
class Material:
    color: vec3  # type: ignore
    specular: f32  # type: ignore
