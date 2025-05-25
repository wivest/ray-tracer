from imports.common import *

from .input import *

from camera.camera import Camera


SENSIVITY = 0.1
ROTATION = ti.math.pi
ANGLE = ti.math.pi * 2 / 3


class App:

    def __init__(self, name: str, size: tuple[int, int], objects: StructField):
        self.window = ti.GUI(name, size, fast_gui=True)
        self.window.fps_limit = 1000
        self.camera = Camera(size, ANGLE, 1024)
        self.objects = objects

        self.input = Input(self.window)

    def run(self):
        while self.window.running:
            self.__handle_events()

            if self.camera.mode[None]:
                self.camera.preview(self.objects)
            else:
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

        if self.input.is_action_just_pressed(MODE):
            self.camera.mode[None] = not self.camera.mode[None]
            self.camera.reset_samples()

        x_axis = self.input.get_axis(LEFT, RIGHT)
        self.camera.transform.move_x(x_axis * SENSIVITY)

        y_axis = self.input.get_axis(DOWN, UP)
        self.camera.transform.move_y(y_axis * SENSIVITY)

        z_axis = self.input.get_axis(FORWARD, BACKWARD)
        self.camera.transform.move_z(z_axis * SENSIVITY)

        x_axis_flat = self.input.get_axis(LEFT_FLAT, RIGHT_FLAT)
        self.camera.transform.move_flat_x(x_axis_flat * SENSIVITY)

        y_axis_global = self.input.get_axis(DOWN_GLOBAL, UP_GLOBAL)
        self.camera.transform.move_global_y(y_axis_global * SENSIVITY)

        z_axis_flat = self.input.get_axis(FORWARD_FLAT, BACKWARD_FLAT)
        self.camera.transform.move_flat_z(z_axis_flat * SENSIVITY)

        if (
            abs(x_axis)
            + abs(y_axis)
            + abs(z_axis)
            + abs(x_axis_flat)
            + abs(y_axis_global)
            + abs(z_axis_flat)
            > 0
        ):
            self.camera.reset_samples()
