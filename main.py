from cli import get_args

args = get_args()

from imports.common import *

from app.app import App
from model.scene import GLTFException
from camera.lenses.render import Render


ti.init(arch=ti.gpu)
try:
    app = App("Ray Tracing", args.filename, (args.width, args.height))
    app.scene.active_cam = args.camera
    Render.samples = args.samples
    Render.hits = args.iters
    Render.sky = vec3(*args.sky)

    if args.render:
        app.run_render(args.render)
    else:
        app.run()
except GLTFException as e:
    print(f"[Error] {e}")
