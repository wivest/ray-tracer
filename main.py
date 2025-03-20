import taichi as ti
from app.app import App

SIZE = (1080, 720)

ti.init()

app = App("Ray Tracing", SIZE)
app.run()
