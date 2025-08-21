from imports.common import *

from .bounding_box import BoundingBox


@ti.dataclass
class BVH:
    aabb: BoundingBox  # type: ignore
    children: int
    start: int
    count: int
