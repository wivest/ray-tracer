import taichi as ti
from taichi import Vector

from app.app import App
from model.sphere import Sphere


ti.init()

SIZE = (1080, 720)
SPHERES = Sphere.field(shape=3)
SPHERES[0] = Sphere(10, Vector((50, 0, 0)), Vector((1, 1, 0)))
SPHERES[1] = Sphere(10, Vector((25, 0, 0)), Vector((1, 1, 0)))
SPHERES[2] = Sphere(10, Vector((25, 0, 25)), Vector((1, 1, 0)))


app = App("Ray Tracing", SIZE, SPHERES)
app.run()
