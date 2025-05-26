import taichi as ti

from app.app import App
from model.spatial import Spatial


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
SCENE_PATH = "./scene/"


spatial = Spatial(SCENE_PATH, "untitled.obj")

app = App("Ray Tracing", SIZE, spatial.triangles)
app.run()
