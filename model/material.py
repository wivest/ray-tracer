from imports.common import *


@ti.dataclass
class Material:
    diffuse: vec3  # type: ignore
    specular: vec3  # type: ignore
    emmision: vec3  # type: ignore
