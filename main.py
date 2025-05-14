import taichi as ti

from app.app import App
from app.spatial import Spatial


ti.init(arch=ti.gpu)

SIZE = (1080, 720)


spatial = Spatial("untitled.obj")

app = App("Ray Tracing", SIZE, spatial.triangles)
app.run()
