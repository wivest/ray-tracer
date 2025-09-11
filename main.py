import argparse
import taichi as ti

from app.app import App
from model.scene import Scene


ti.init(arch=ti.gpu)

SIZE = (1080, 720)
DEFAULT_GLTF = "./scene/untitled.gltf"

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default=DEFAULT_GLTF)
args = parser.parse_args()


scene = Scene(args.filename)

triangles, bvhs = scene.export()

app = App("Ray Tracing", SIZE, triangles, bvhs, DEFAULT_GLTF)
app.run()
