import taichi as ti
from taichi import StructField

from .input import *
from model.camera import Camera


ROTATION = ti.math.pi
ANGLE = ti.math.pi * 2 / 3


class App:

    def __init__(self, name: str, size: tuple[int, int], objects: StructField):
        self.window = ti.GUI(name, size, fast_gui=True)
        self.window.fps_limit = 1000
        self.camera = Camera(size, ANGLE, 64)
        self.objects = objects

        self.input = Input(self.window)
        self.__rotating = False
        self.__cursor = self.window.get_cursor_pos()

    def run(self):
        while self.window.running:
            self.__handle_events()
            if self.__rotating:
                delta = self.__get_cursor_delta()
                self.camera.transform.rotate_y(delta[0] * ROTATION * 2)
                self.camera.transform.rotate_local_x(-delta[1] * ROTATION)
                self.camera.reset_samples()

            if self.camera._ready[None] < self.camera.samples:
                self.camera.render(self.objects)
            self.window.set_image(self.camera.pixels)
            self.window.show()

    def __handle_events(self):
        self.input.read_events()
        x_axis = self.input.get_axis(LEFT, RIGHT)
        if x_axis != 0.0:
            self.camera.transform.move_x(x_axis)
            self.camera.reset_samples()

        for event in self.window.get_events():
            if event.key == ti.GUI.LMB:
                if event.type == ti.GUI.RELEASE:
                    self.__rotating = False
                else:
                    self.__rotating = True
                    self.__get_cursor_delta()

            elif event.key == "a":
                if ti.GUI.SHIFT in event.modifier:  # type: ignore
                    self.camera.transform.move_flat_x(-1)
                else:
                    pass
                # self.camera.transform.move_x(-1)
                self.camera.reset_samples()
            elif event.key == "d":
                if ti.GUI.SHIFT in event.modifier:  # type: ignore
                    self.camera.transform.move_flat_x(1)
                else:
                    pass
                # self.camera.transform.move_x(1)
                self.camera.reset_samples()

            elif event.key == "w":
                if ti.GUI.SHIFT in event.modifier:  # type: ignore
                    self.camera.transform.move_global_z(-1)
                else:
                    self.camera.transform.move_z(-1)
                self.camera.reset_samples()
            elif event.key == "s":
                if ti.GUI.SHIFT in event.modifier:  # type: ignore
                    self.camera.transform.move_global_z(1)
                else:
                    self.camera.transform.move_z(1)
                self.camera.reset_samples()

            elif event.key == "e":
                if ti.GUI.SHIFT in event.modifier:  # type: ignore
                    self.camera.transform.move_global_y(1)
                else:
                    self.camera.transform.move_y(1)
                self.camera.reset_samples()
            elif event.key == "x":
                if ti.GUI.SHIFT in event.modifier:  # type: ignore
                    self.camera.transform.move_global_y(-1)
                else:
                    self.camera.transform.move_y(-1)
                self.camera.reset_samples()

    def __get_cursor_delta(self, update=True) -> tuple[float, float]:
        actual = self.window.get_cursor_pos()
        delta = (actual[0] - self.__cursor[0], actual[1] - self.__cursor[1])
        if update:
            self.__cursor = actual
        return delta
