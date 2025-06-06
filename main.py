import sys
import taichi as ti

from app.app import App
from model.spatial import Spatial
from model.setup import Setup


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
DEFAULT_SCENE = "./scene/"
DEFAULT_OBJ = DEFAULT_SCENE + "untitled.obj"
DEFAULT_SETUP = DEFAULT_SCENE + "setup"


obj_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_OBJ
spatial = Spatial(obj_path)
camera_transform = Setup.get_camera_transform(DEFAULT_SETUP)

app = App("Ray Tracing", SIZE, spatial.export(), camera_transform)
app.run()
