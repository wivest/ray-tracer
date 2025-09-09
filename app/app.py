from imports.common import *

from .input import *

from camera.camera import Camera
from camera.lenses import Preview, Render


SENSIVITY = 0.1
ROTATION = ti.math.pi


class App:

    def __init__(
        self,
        name: str,
        size: tuple[int, int],
        triangles: StructField,
        bvhs: StructField,
        gltf_path: str,
    ):
        self.camera = Camera(size, gltf_path)

        self.preview = Preview(self.camera.size, self.camera.transform)
        self.render = Render(self.camera.size, 1024, self.camera.transform)
        self.camera.lens = self.preview

        self.window = ti.GUI(name, self.camera.size, fast_gui=True)
        self.window.fps_limit = 1000

        self.triangles = triangles
        self.bvhs = bvhs
        self.input = Input(self.window)
        self.mode = True

    def run(self):
        while self.window.running:
            self.__handle_events()

            self.camera.render(self.triangles, self.bvhs)
            self.window.set_image(self.camera.pixels)
            self.window.show()

    def render_image(self):
        self.camera.render(self.triangles, self.bvhs)
        self.window.set_image(self.camera.pixels)
        self.window.show()

    def __handle_events(self):
        self.input.read_events()

        delta = self.input.get_cursor_delta()
        if self.input.is_action_pressed(LMB):
            self.camera.transform.rotate_y(delta[0] * ROTATION * 2)
            self.camera.transform.rotate_local_x(-delta[1] * ROTATION)
            self.render.reset_samples()

        if self.input.is_action_just_pressed(MODE):
            self.mode = not self.mode
            if self.mode:
                self.camera.lens = self.preview
            else:
                self.camera.lens = self.render
            self.render.reset_samples()

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
            self.render.reset_samples()
