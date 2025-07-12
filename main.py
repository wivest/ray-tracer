import sys
import taichi as ti
from pygltflib import GLTF2

from app.app import App
from model.scene import Scene


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
DEFAULT_GLTF = "./scene/untitled.gltf"

gltf_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_GLTF
spatial = Scene(gltf_path)

app = App("Ray Tracing", SIZE, spatial.export(), DEFAULT_GLTF)
app.run()
