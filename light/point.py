from imports.common import *

from .light import Light


@ti.dataclass
class Point(Light):
    color: vec3  # type: ignore
