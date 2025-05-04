from imports.common import *


@ti.dataclass
class Colored:
    color: vec3  # type: ignore

    @ti.func
    def get(self, direction: vec3) -> Vector:  # type: ignore
        return self.color
