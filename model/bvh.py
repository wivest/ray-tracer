from imports.common import *

from .aabb import AABB


@ti.dataclass
class BVH:
    aabb: AABB  # type: ignore
    left: int
    right: int
    start: int
    count: int
