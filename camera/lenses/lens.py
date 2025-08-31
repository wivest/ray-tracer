from abc import ABC, abstractmethod

from imports.common import *

from ..transform import Transform
from ..ray import Ray
from ..hit_info import HitInfo
from ..tonemapping import aces
from model.spatial import Spatial


class Lens(ABC):

    transform: Transform
    fov: float

    @abstractmethod
    def render(
        self, pixels: MatrixField, triangles: StructField, bvhs: StructField
    ): ...

    @ti.func
    def _cast_ray(self, ray: Ray, triangles: ti.template(), bvhs: ti.template()) -> HitInfo:  # type: ignore
        hit_info = HitInfo(distance=ti.math.inf)
        stack = ti.Vector.zero(ti.i32, 2 * Spatial.BVH_DEPTH)
        top = 0

        while top >= 0:
            bvh = bvhs[stack[top]]
            top -= 1

            if bvh.aabb.intersects(ray):
                # BVH is leaf
                if bvh.left == 0:
                    hit_info_bvh = ray.cast2(triangles, bvh.start, bvh.count)
                    if hit_info_bvh.hit and hit_info_bvh.distance < hit_info.distance:  # type: ignore
                        hit_info = hit_info_bvh

                # BVH is inner node
                else:
                    dst_far = dst_left = bvhs[bvh.left].aabb.distance(ray)
                    dst_close = dst_right = bvhs[bvh.right].aabb.distance(ray)
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

    @ti.kernel
    def render_sample_tmp(self, pixels: ti.template(), triangles: ti.template(), bvhs: ti.template()):  # type: ignore
        center_x = pixels.shape[0] / 2
        center_y = pixels.shape[1] / 2
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self._cast_ray(ray, triangles, bvhs)
            pixels[x, y] = aces(incoming_light)
