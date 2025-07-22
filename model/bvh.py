from imports.common import *

from .bounding_box import BoundingBox


@ti.dataclass
class AABBwTriangles:
    aabb: BoundingBox  # type: ignore
    start: int
    length: int


@ti.dataclass
class BVH:
    bounding_boxes: ti.template()  # type: ignore
    triangles: ti.template()  # type: ignore
