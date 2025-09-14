from cli import get_args, DEFAULT_GLTF

args = get_args()

import taichi as ti

from app.app import App
from model.scene import Scene


ti.init(arch=ti.gpu)

scene = Scene(args.filename, (args.width, args.height))
app = App("Ray Tracing", scene)
if args.render:
    app.run_render()
else:
    app.run()
