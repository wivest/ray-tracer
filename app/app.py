import taichi as ti

from model.camera import Camera


class App:
    window: ti.GUI
    camera: Camera

    def __init__(self, name: str, size: tuple[int, int]):
        self.window = ti.GUI(name, size, fast_gui=True)
        self.camera = Camera(size)

    def run(self):
        while self.window.running:
            self.camera.transform.rotate_y(0.02)
            self.camera.render()
            self.window.set_image(self.camera.pixels)
            self.window.show()
