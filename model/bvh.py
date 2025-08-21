from imports.common import *

from .aabb import AABB


@ti.dataclass
class BVH:
    aabb: AABB  # type: ignore
    children: int
    start: int
    count: int
