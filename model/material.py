import taichi as ti
from taichi import f32
from taichi.math import vec3


@ti.dataclass
class Material:
    diffuse: vec3  # type: ignore
    specular: vec3  # type: ignore
    emmision: f32  # type: ignore
