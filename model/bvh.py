from imports.common import *


@ti.dataclass
class BVH:
    bounding_boxes: ti.template()  # type: ignore
    triangles: ti.template()  # type: ignore
