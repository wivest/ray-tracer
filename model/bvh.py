from imports.common import *

from .bounding_box import BoundingBox


@ti.dataclass
class BVH:
    aabb: BoundingBox  # type: ignore
    first: int
    second: int
    start: int
    length: int
