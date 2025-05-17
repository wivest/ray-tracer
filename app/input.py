from taichi.ui import GUI

from .action import Action

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
FORWARD = "forward"
BACKWARD = "backward"

LEFT_FLAT = "left_flat"
RIGHT_FLAT = "right_flat"
UP_GLOBAL = "up_global"
DOWN_GLOBAL = "down_global"
FORWARD_FLAT = "forward_flat"
BACKWARD_FLAT = "backward_flat"

LMB = "lbm"

MODE = "mode"

ACTIONS: dict[str, Action] = {
    LEFT: Action("a"),
    RIGHT: Action("d"),
    UP: Action("e"),
    DOWN: Action("x"),
    FORWARD: Action("w"),
    BACKWARD: Action("s"),
    LEFT_FLAT: Action("a", [GUI.SHIFT]),
    RIGHT_FLAT: Action("d", [GUI.SHIFT]),
    UP_GLOBAL: Action("e", [GUI.SHIFT]),
    DOWN_GLOBAL: Action("x", [GUI.SHIFT]),
    FORWARD_FLAT: Action("w", [GUI.SHIFT]),
    BACKWARD_FLAT: Action("s", [GUI.SHIFT]),
    LMB: Action(GUI.LMB),
    MODE: Action("m"),
}


class Input:

    def __init__(self, window: GUI):
        self.window = window

        self.__cursor = self.window.get_cursor_pos()

    def read_events(self):
        for event in self.window.get_events():
            for action in ACTIONS.values():
                action.handle_event(event)

    def is_action_pressed(self, name: str) -> bool:
        action = ACTIONS[name]
        return action.pressed

    def get_axis(self, neg: str, pos: str) -> float:
        negative = 1.0 if ACTIONS[neg].pressed else 0.0
        positive = 1.0 if ACTIONS[pos].pressed else 0.0
        return positive - negative

    def get_cursor_delta(self) -> tuple[float, float]:
        actual = self.window.get_cursor_pos()
        delta = (actual[0] - self.__cursor[0], actual[1] - self.__cursor[1])
        self.__cursor = actual
        return delta
