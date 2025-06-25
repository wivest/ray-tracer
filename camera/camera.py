from pygltflib import GLTF2
from scipy.spatial.transform import Rotation

from imports.common import *

from .tonemapping import aces
from .transform import Transform
from .ray import Ray
from .hit_info import HitInfo

from light.sun import Sun
from sky.colored import Colored


@ti.data_oriented
class Camera:

    def __init__(
        self,
        size: tuple[int, int],
        gltf_path: str,
        angle: float,
        samples: int,
    ):
        self.transform = self.__get_camera_data(gltf_path)
        self.pixels = Vector.field(3, f32, size)
        self.fov: float = size[1] / ti.tan(angle / 2)
        self.sky = Colored(Vector((1.0, 1.0, 1.0)))

        self.lights = Sun.field(shape=(2))
        self.lights[0] = Sun(Vector((5, 5, 5)), Vector((-1, -1, -1)))
        self.lights[1] = Sun(Vector((5, 5, 5)), Vector((1, -1, 1)))

        self.samples = samples
        self.mode: Field = ti.field(bool, ())
        self.mode[None] = True

        self._sampled = Vector.field(3, f32, size)
        self._sampled.fill(0.0)
        self._ready: Field = ti.field(int, ())
        self._ready[None] = 0

    def __get_camera_data(self, path: str):
        data = GLTF2().load(path)
        if data == None:
            raise Exception()
        scene = data.scenes[data.scene]
        if scene.nodes == None:
            raise Exception()

        t = []
        r = []
        for i in scene.nodes:
            node = data.nodes[i]
            if node.camera != None:
                t = node.translation
                r = node.rotation

        if t == None or r == None:
            raise Exception()

        return self.__convert_transform(t, r)

    def __convert_transform(
        self, translation: list[float], rotation: list[float]
    ) -> Transform:
        if len(translation) != 3:
            raise Exception()

        origin = (translation[0], translation[1], translation[2])
        mat = Rotation.from_quat(rotation).as_matrix()
        bas = tuple(tuple(i) for i in mat.tolist())

        return Transform(origin, bas)  # type: ignore

    @ti.kernel
    def reset_samples(self):
        self._sampled.fill(0.0)
        self._ready[None] = 0

    @ti.kernel
    def preview(self, objects: ti.template()):  # type: ignore
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self.get_preview_color(ray, objects)
            self.pixels[x, y] = aces(incoming_light)

    @ti.func
    def get_preview_color(self, ray: Ray, objects: ti.template()) -> Vector:  # type: ignore
        incoming_light = self.sky.get(ray.direction)  # type: ignore

        hit_info = ray.cast(objects)
        if hit_info.hit:
            sin = ti.abs(ti.math.dot(ray.direction, hit_info.normal))
            incoming_light = sin * (
                hit_info.material.emmision + hit_info.material.diffuse
            )

        return incoming_light

    @ti.kernel
    def render(self, objects: ti.template()):  # type: ignore
        center_x = self.pixels.shape[0] / 2
        center_y = self.pixels.shape[1] / 2
        self._ready[None] += 1

        ready = self._ready[None]
        basis = self.transform.basis[None]
        origin = self.transform.origin[None]

        for x, y in self.pixels:
            pixel = Vector((x - center_x, y - center_y, -self.fov), f32).normalized()
            direction = basis @ pixel
            ray = Ray(origin, direction)

            incoming_light = self.get_color(ray, objects, 6)
            self._sampled[x, y] += aces(incoming_light)
            self.pixels[x, y] = self._sampled[x, y] / ready

    @ti.func
    def get_color(self, ray: Ray, objects: ti.template(), hits: int) -> Vector:  # type: ignore
        incoming_light = Vector((0.0, 0.0, 0.0))
        ray_color = Vector((1.0, 1.0, 1.0))

        for i in range(hits):
            hit_info = ray.cast(objects)
            if not hit_info.hit:
                incoming_light += ray_color * self.sky.get(ray.direction)  # type: ignore
                break

            ray = self._bounce_ray(ray, hit_info)
            sin = ti.math.dot(ray.direction, hit_info.normal)
            ray_color = sin * ray_color * hit_info.material.diffuse
            incoming_light += ray_color * (
                hit_info.material.emmision
                + self.sample_direct_light(
                    hit_info.point, objects, self.lights, hit_info.normal
                )
            )

        return incoming_light

    @ti.func
    def _bounce_ray(self, ray: Ray, hit_info: HitInfo) -> Ray:  # type: ignore
        specular = ti.math.reflect(ray.direction, hit_info.normal)
        diffuse = self._random_hemisphere(hit_info.normal)
        ray_dir = ti.math.mix(
            diffuse, specular, hit_info.material.specular
        ).normalized()
        return Ray(hit_info.point, ray_dir)

    @ti.func
    def _random_hemisphere(self, normal: vec3) -> Vector:  # type: ignore
        x = ti.randn()
        y = ti.randn()
        z = ti.randn()
        dir = vec3(x, y, z)
        if ti.math.dot(dir, normal) < 0:
            dir *= -1
        return dir.normalized()

    @ti.func
    def sample_direct_light(self, point: vec3, objects: ti.template(), lights: ti.template(), normal: vec3) -> Vector:  # type: ignore
        visible = Vector((0.0, 0.0, 0.0))

        for i in range(lights.shape[0]):
            light = lights[i]
            ray = light.get_ray(point)
            sin = ti.math.dot(ray.direction, normal)

            if not ray.cast(objects).hit:
                visible += sin * light.color

        return visible
