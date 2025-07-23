from imports.common import *

from .bounding_box import BoundingBox


@ti.dataclass
class AABBwTriangles:
    aabb: BoundingBox  # type: ignore
    first: int
    second: int
    start: int
    length: int


@ti.dataclass
class BVH:
    bounding_boxes: ti.template()  # type: ignore
    triangles: ti.template()  # type: ignore
