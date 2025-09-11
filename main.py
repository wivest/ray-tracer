import argparse
import taichi as ti

from app.app import App
from model.scene import Scene


SIZE = (1080, 720)
DEFAULT_GLTF = "./scene/untitled.gltf"

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--render", action="store_true")
parser.add_argument("-x", "--width", default=SIZE[0], type=int)
parser.add_argument("-y", "--height", default=SIZE[1], type=int)
parser.add_argument("filename", nargs="?", default=DEFAULT_GLTF)
args = parser.parse_args()


ti.init(arch=ti.gpu)

scene = Scene(args.filename)
triangles, bvhs = scene.export()

app = App("Ray Tracing", (args.width, args.height), triangles, bvhs, DEFAULT_GLTF)
if args.render:
    app.run_render()
else:
    app.run()
