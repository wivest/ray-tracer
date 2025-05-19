from taichi.ui import GUI


class Action:

    def __init__(self, key: str, modifiers: list[str] = []):
        self.key = key
        self.modifiers = modifiers
        self.pressed: bool = False
        self.__just_pressed: bool = False

    def handle_event(self, event: GUI.Event):
        if self.key == event.key:
            mod = self.__check_modifiers(event.modifier)  # type: ignore
            self.__just_pressed = self.__just_pressed or not self.pressed
            self.pressed = event.type == GUI.PRESS and mod

    def is_just_pressed(self):
        just = self.__just_pressed
        self.__just_pressed = False
        return just and self.pressed

    def __check_modifiers(self, modifiers: list[str]) -> bool:
        if len(self.modifiers) != len(modifiers):
            return False
        for mod in self.modifiers:
            if not mod in modifiers:
                return False
        return True
