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

    def run(self):
        while self.window.running:
            self.__handle_events()

            if self.camera._ready[None] < self.camera.samples:
                self.camera.render(self.objects)
            self.window.set_image(self.camera.pixels)
            self.window.show()

    def __handle_events(self):
        self.input.read_events()

        delta = self.input.get_cursor_delta()
        if self.input.is_action_pressed(LMB):
            self.camera.transform.rotate_y(delta[0] * ROTATION * 2)
            self.camera.transform.rotate_local_x(-delta[1] * ROTATION)
            self.camera.reset_samples()

        x_axis = self.input.get_axis(LEFT, RIGHT)
        if x_axis != 0.0:
            self.camera.transform.move_x(x_axis)
            self.camera.reset_samples()

        y_axis = self.input.get_axis(DOWN, UP)
        if y_axis != 0.0:
            self.camera.transform.move_y(y_axis)
            self.camera.reset_samples()

        z_axis = self.input.get_axis(FORWARD, BACKWARD)
        if z_axis != 0.0:
            self.camera.transform.move_z(z_axis)
            self.camera.reset_samples()

        x_axis_flat = self.input.get_axis(LEFT_FLAT, RIGHT_FLAT)
        if x_axis_flat != 0.0:
            self.camera.transform.move_flat_x(x_axis_flat)
            self.camera.reset_samples()

        y_axis_global = self.input.get_axis(DOWN_GLOBAL, UP_GLOBAL)
        if y_axis_global != 0.0:
            self.camera.transform.move_global_y(y_axis_global)
            self.camera.reset_samples()

        z_axis_flat = self.input.get_axis(FORWARD_FLAT, BACKWARD_FLAT)
        if z_axis_flat != 0.0:
            self.camera.transform.move_flat_z(z_axis_flat)
            self.camera.reset_samples()
