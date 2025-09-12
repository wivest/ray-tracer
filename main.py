from cli import get_args, DEFAULT_GLTF

args = get_args()

import taichi as ti

from app.app import App
from model.scene import Scene


ti.init(arch=ti.gpu)

scene = Scene(args.filename)
triangles, bvhs = scene.export()

app = App("Ray Tracing", (args.width, args.height), triangles, bvhs, args.filename)
if args.render:
    app.run_render()
else:
    app.run()
