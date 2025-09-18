from cli import get_args

args = get_args()

import taichi as ti

from app.app import App


ti.init(arch=ti.gpu)

app = App("Ray Tracing", args.filename, (args.width, args.height))
if args.render:
    app.run_render()
else:
    app.run()
