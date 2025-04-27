import taichi as ti

from taichi import Vector
from taichi.math import vec3


@ti.func
def raw(incoming_light: vec3) -> Vector:  # type: ignore
    return incoming_light
