from imports.common import *

from .input import *

from model.scene import Scene
from camera.lenses import Render


SENSIVITY = 0.1
ROTATION = ti.math.pi


class App:

    def __init__(self, name: str, path: str, camera_size: tuple[int, int]):
        self.scene = Scene(path, camera_size)
        self.window = ti.GUI(name, camera_size, fast_gui=True)
        self.window.fps_limit = 1000
        self.input = Input(self.window)

    def run(self):
        while self.window.running:
            self.__handle_events()

            self.scene.camera.render(
                self.scene.tris, self.scene.bvhs, self.scene.lights
            )
            self.window.set_image(self.scene.camera.pixels)
            self.window.show()

    def run_render(self, filename: str):
        self.scene.camera.lens = self.scene.camera.render_lens
        rendered = 0
        saved = False

        while self.window.running:
            finished = self.scene.camera.render(
                self.scene.tris, self.scene.bvhs, self.scene.lights
            )
            if not finished:
                rendered += 1
                print(f"\r[{rendered}/{Render.samples}] Samples rendered", end="")
            if not saved and finished:
                print(f"\n[Rendering] Render saved to {filename} (ready to quit)")
                ti.tools.imwrite(self.scene.camera.pixels, filename)
                saved = True

            self.window.set_image(self.scene.camera.pixels)
            self.window.show()

        if not saved:
            print(f"\n[Rendering] Unfinished render saved to {filename}")
            ti.tools.imwrite(self.scene.camera.pixels, filename)

    def __handle_events(self):
        self.input.read_events()

        delta = self.input.get_cursor_delta()

        if self.input.is_action_just_pressed(NEXT_CAMERA):
            self.scene.active_cam += 1
            self.scene.active_cam %= len(self.scene.cameras)

        if self.input.is_action_pressed(LMB):
            self.scene.camera.transform.rotate_y(delta[0] * ROTATION * 2)
            self.scene.camera.transform.rotate_local_x(-delta[1] * ROTATION)
            self.scene.camera.render_lens.reset_samples()

        if self.input.is_action_just_pressed(MODE):
            self.scene.camera.is_preview_mode = not self.scene.camera.is_preview_mode
            if self.scene.camera.is_preview_mode:
                self.scene.camera.lens = self.scene.camera.preview_lens
            else:
                self.scene.camera.lens = self.scene.camera.render_lens
                self.scene.camera.render_lens.reset_samples()

        x_axis = self.input.get_axis(LEFT, RIGHT)
        self.scene.camera.transform.move_x(x_axis * SENSIVITY)

        y_axis = self.input.get_axis(DOWN, UP)
        self.scene.camera.transform.move_y(y_axis * SENSIVITY)

        z_axis = self.input.get_axis(FORWARD, BACKWARD)
        self.scene.camera.transform.move_z(z_axis * SENSIVITY)

        x_axis_flat = self.input.get_axis(LEFT_FLAT, RIGHT_FLAT)
        self.scene.camera.transform.move_flat_x(x_axis_flat * SENSIVITY)

        y_axis_global = self.input.get_axis(DOWN_GLOBAL, UP_GLOBAL)
        self.scene.camera.transform.move_global_y(y_axis_global * SENSIVITY)

        z_axis_flat = self.input.get_axis(FORWARD_FLAT, BACKWARD_FLAT)
        self.scene.camera.transform.move_flat_z(z_axis_flat * SENSIVITY)

        if (
            abs(x_axis)
            + abs(y_axis)
            + abs(z_axis)
            + abs(x_axis_flat)
            + abs(y_axis_global)
            + abs(z_axis_flat)
            > 0
        ):
            self.scene.camera.render_lens.reset_samples()
