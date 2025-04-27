import taichi as ti

from taichi import Vector
from taichi.math import vec3


@ti.func
def raw(incoming_light: vec3) -> Vector:  # type: ignore
    return incoming_light


@ti.func
def aces(incoming_light: vec3) -> Vector:  # type: ignore
    incoming_light *= 0.6
    a = 2.51
    b = 0.03
    c = 2.43
    d = 0.59
    e = 0.14
    return (incoming_light * (a * incoming_light + b)) / (
        incoming_light * (c * incoming_light + d) + e
    )
