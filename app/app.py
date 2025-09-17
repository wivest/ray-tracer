from imports.common import *

from .input import *

from camera.lenses import Preview, Render
from model.scene import Scene


SENSIVITY = 0.1
ROTATION = ti.math.pi


class App:

    def __init__(self, name: str, scene: Scene):
        self.scene = scene
        t = self.scene.camera.transform
        self.preview_lens = Preview(self.scene.camera.size, t)
        self.render_lens = Render(self.scene.camera.size, t, 64, scene.lights)
        self.scene.camera.lens = self.preview_lens

        self.window = ti.GUI(name, self.scene.camera.size, fast_gui=True)
        self.window.fps_limit = 1000
        self.input = Input(self.window)
        self.mode = True

    def run(self):
        while self.window.running:
            self.__handle_events()

            self.scene.camera.render(self.scene.tris, self.scene.bvhs)
            self.window.set_image(self.scene.camera.pixels)
            self.window.show()

    def run_render(self, filename: str = "render.png"):
        self.scene.camera.lens = self.render_lens
        saved = False

        while self.window.running:
            finished = self.scene.camera.render(self.scene.tris, self.scene.bvhs)
            if not saved and finished:
                print(f"[Render] Render saved to {filename}")
                ti.tools.imwrite(self.scene.camera.pixels, filename)
                saved = True

            self.window.set_image(self.scene.camera.pixels)
            self.window.show()

        if not saved:
            print(f"[Render] Unfinished render saved to {filename}")
            ti.tools.imwrite(self.scene.camera.pixels, filename)

    def __handle_events(self):
        self.input.read_events()

        delta = self.input.get_cursor_delta()
        if self.input.is_action_pressed(LMB):
            self.scene.camera.transform.rotate_y(delta[0] * ROTATION * 2)
            self.scene.camera.transform.rotate_local_x(-delta[1] * ROTATION)
            self.render_lens.reset_samples()

        if self.input.is_action_just_pressed(MODE):
            self.mode = not self.mode
            if self.mode:
                self.scene.camera.lens = self.preview_lens
            else:
                self.scene.camera.lens = self.render_lens
            self.render_lens.reset_samples()

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
            self.render_lens.reset_samples()
