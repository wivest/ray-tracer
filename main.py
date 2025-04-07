import taichi as ti
from taichi import Vector

from app.app import App
from model.sphere import Sphere
from model.material import Material


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
SPHERES = Sphere.field(shape=5)
SPHERES[0] = Sphere(10, Vector((50, 0, 0)), Material(Vector((1.0, 0.25, 0.25)), 0.5))
SPHERES[1] = Sphere(10, Vector((25, 0, 0)), Material(Vector((0.25, 1.0, 0.25)), 0.5))
SPHERES[2] = Sphere(10, Vector((25, 0, 25)), Material(Vector((0.25, 0.25, 1.0)), 0.5))
SPHERES[3] = Sphere(10, Vector((50, 0, 25)), Material(Vector((1.0, 1.0, 1.0)), 1.0))
SPHERES[4] = Sphere(490, Vector((0, -500, 0)), Material(Vector((1.0, 1.0, 1.0)), 0.0))


app = App("Ray Tracing", SIZE, SPHERES)
app.run()
