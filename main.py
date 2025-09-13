from cli import get_args, DEFAULT_GLTF

args = get_args()

import taichi as ti

from app.app import App
from model.scene import Scene


ti.init(arch=ti.gpu)

scene = Scene(args.filename)
app = App("Ray Tracing", (args.width, args.height), scene, args.filename)
if args.render:
    app.run_render()
else:
    app.run()
