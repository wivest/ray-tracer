import sys
import taichi as ti
from pygltflib import GLTF2

from app.app import App
from model.spatial import Spatial


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
DEFAULT_SCENE = "./scene/"
DEFAULT_GLTF = DEFAULT_SCENE + "untitled.gltf"

gltf_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_GLTF
gltf = GLTF2().load(gltf_path)
if gltf == None:
    raise Exception()
spatial = Spatial(gltf.meshes[0], gltf)

app = App("Ray Tracing", SIZE, spatial.export(), DEFAULT_GLTF)
app.run()
