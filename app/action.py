from taichi.ui import GUI


class Action:

    def __init__(self, key: str):
        self.key = key
        self.pressed: bool = False

    def handle_event(self, event: GUI.Event):
        if self.key == event.key:
            self.pressed = event.type == GUI.PRESS
