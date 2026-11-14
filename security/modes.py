


class ModeManager:
    MODES = {
        "home": set(),
        "night": {"door", "window"},
        "away": {"motion", "door", "window"}
    }

    def __init__(self):
        self.current_mode = "home"

    def set_mode(self, mode):
        if mode not in ModeManager.MODES:
            return False

        self.current_mode = mode
        return True

    def get_mode(self):
        return self.current_mode

    def is_sensor_monitored(self, sensor_type):
        return sensor_type in self.MODES[self.current_mode]