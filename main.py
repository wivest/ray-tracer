import sys
import taichi as ti

from app.app import App
from model.spatial import Spatial
from model.scene import Scene


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
SCENE_PATH = "./scene/"
DEFAULT_OBJ = "untitled.obj"


scene = Scene(SCENE_PATH)
obj_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_OBJ
spatial = Spatial(SCENE_PATH, obj_path)

app = App("Ray Tracing", SIZE, spatial.export())
app.run()
