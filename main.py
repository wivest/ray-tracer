import taichi as ti
from taichi import Vector

from app.app import App
from model.sphere import Sphere


ti.init()

SIZE = (1080, 720)
SPHERES = Sphere.field(shape=1)
SPHERES[0] = Sphere(10, Vector((100, 0, 0)), Vector((1, 1, 0)))


app = App("Ray Tracing", SIZE, SPHERES)
app.run()
