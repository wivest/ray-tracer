import sys
import taichi as ti

from app.app import App
from model.spatial import Spatial


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
DEFAULT_OBJ = "./scene/untitled.obj"


obj_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_OBJ
spatial = Spatial(obj_path)

app = App("Ray Tracing", SIZE, spatial.export())
app.run()
