import sys
import taichi as ti

from app.app import App
from model.scene import Scene


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
DEFAULT_GLTF = "./scene/untitled.gltf"

gltf_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_GLTF
scene = Scene(gltf_path)

triangles, bvhs, bvh_roots = scene.export()

app = App("Ray Tracing", SIZE, triangles, bvhs, bvh_roots, DEFAULT_GLTF)
app.run()
