import taichi as ti


class App:
    window: ti.GUI

    def __init__(self, name: str, size: tuple[int, int]):
        self.window = ti.GUI(name, size, fast_gui=True)

    def run(self):
        while self.window.running:
            self.window.show()
