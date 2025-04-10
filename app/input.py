from taichi.ui import GUI

from .action import Action

LEFT = "left"
RIGHT = "right"

ACTIONS: dict[str, Action] = {LEFT: Action("a"), RIGHT: Action("d")}


class Input:

    def __init__(self, window: GUI):
        self.window = window

    def read_events(self):
        for event in self.window.get_events():
            for action in ACTIONS.values():
                action.handle_event(event)

    def get_axis(self, neg: str, pos: str) -> float:
        negative = 1.0 if ACTIONS[neg].pressed else 0.0
        positive = 1.0 if ACTIONS[pos].pressed else 0.0
        return positive - negative
