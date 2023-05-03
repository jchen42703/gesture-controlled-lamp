from lamp_common import SUPPORTED_GESTURES, OPERATIONS
from lamp_driver import LampDriver


class LampService:
    """Controls the LampDriver based on the recognized gestures.
    """

    def __init__(self) -> None:
        self.lamp_driver = LampDriver()
        self.default_hue = 1
        self.default_saturation = 0.5
        self.brightness = 0

    def get_operation_from_gesture(self, gesture: str) -> str:
        """TODO: change to read from config
        """
        if gesture == SUPPORTED_GESTURES[0]:
            return OPERATIONS[0]
        elif gesture == SUPPORTED_GESTURES[1]:
            return OPERATIONS[0]
        elif gesture == SUPPORTED_GESTURES[2]:
            return OPERATIONS[1]
        else:
            return OPERATIONS[2]

    def increase_brightness(self):
        new_brightness = self.brightness + 0.1 if self.brightness > 0 else 0.1
        new_brightness = min(1, new_brightness)
        self.brightness = new_brightness
        print("Increaseing brightness to ", new_brightness)
        self.lamp_driver.set_lamp_state(self.default_hue, self.default_saturation,
                                        new_brightness, True)

    def decrease_brightness(self):
        new_brightness = self.brightness - 0.1
        new_brightness = max(new_brightness, 0)
        self.brightness = new_brightness
        print("Decreasing brightness to ", new_brightness)
        self.lamp_driver.set_lamp_state(self.default_hue, self.default_saturation,
                                        new_brightness, True)

    def run_op(self, operation: str):
        if operation == "Do nothing":
            return

        if operation == "Increase Brightness":
            self.increase_brightness()
            return

        if operation == "Decrease Brightness":
            self.decrease_brightness()
            return

    def run_from_gesture(self, gesture: str):
        operation = self.get_operation_from_gesture(gesture)
        self.run_op(operation)
        return gesture
