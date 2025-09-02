from imports.common import *

from .hit_info import HitInfo
from model.material import Material
from model.spatial import Spatial


TRESHHOLD = 0.001


@ti.dataclass
class Ray:
    origin: vec3  # type: ignore
    direction: vec3  # type: ignore

    @ti.func
    def cast(self, triangles: ti.template(), bvhs: ti.template(), bvh_roots: ti.template()) -> HitInfo:  # type: ignore
        hit_info = HitInfo(distance=ti.math.inf)
        stack = ti.Vector.zero(ti.i32, 2 * Spatial.BVH_DEPTH)

        for i in range(bvh_roots.shape[0]):
            root = bvh_roots[i]
            stack[0] = root
            top = 0

            while top >= 0:
                bvh = bvhs[stack[top]]
                top -= 1

                if bvh.aabb.intersects(self):
                    # BVH is leaf
                    if bvh.left == 0:
                        hit_info_bvh = self._cast_triangles(
                            triangles, bvh.start, bvh.count
                        )
                        if hit_info_bvh.hit and hit_info_bvh.distance < hit_info.distance:  # type: ignore
                            hit_info = hit_info_bvh

                    # BVH is inner node
                    else:
                        dst_far = dst_left = bvhs[bvh.left].aabb.distance(self)
                        dst_close = dst_right = bvhs[bvh.right].aabb.distance(self)
                        farther = bvh.left
                        closer = bvh.right
                        if dst_left < dst_right:
                            dst_far = dst_right
                            dst_close = dst_left
                            farther = bvh.right
                            closer = bvh.left

                        if dst_far < hit_info.distance:  # type: ignore
                            stack[top + 1] = farther
                            top += 1
                        if dst_close < hit_info.distance:  # type: ignore
                            stack[top + 1] = closer
                            top += 1

        return hit_info

    @ti.func
    def _cast_triangles(self, triangles: ti.template(), start: int, count: int) -> HitInfo:  # type: ignore
        point = self.origin
        normal = vec3(0)
        material = Material()
        hit = False

        nearest = ti.math.inf
        for i in range(start, start + count):
            coef = triangles[i].intersects(self)
            if coef > TRESHHOLD and coef < nearest:
                nearest = coef
                hit = True

                material = triangles[i].material
                point = self.origin + self.direction * coef
                normal = triangles[i].normal

        return HitInfo(hit, nearest, point, normal, material)
