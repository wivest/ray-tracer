from cli import get_args

args = get_args()

from imports.common import *

from app.app import App
from camera.lenses.render import Render


ti.init(arch=ti.gpu)

app = App("Ray Tracing", args.filename, (args.width, args.height))
Render.hits = args.iters
Render.sky = vec3(*args.sky)
if args.render:
    app.run_render()
else:
    app.run()
