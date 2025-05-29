import taichi as ti

from app.app import App
from model.spatial import Spatial
from model.scene import Scene


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
SCENE_PATH = "./scene/"


scene = Scene(SCENE_PATH)
spatial = Spatial(SCENE_PATH, "untitled.obj")

app = App("Ray Tracing", SIZE, spatial.export())
app.run()
