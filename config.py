import yaml
from dataclasses import dataclass


@dataclass
class LampGestureConfig:
    """Mapping from the function to the gesture
    """
    on_gesture: str | None
    off_gesture: str | None
    # Replace with number gestures
    increase_brightness_gesture: str | None
    decrease_brightness_gesture: str | None


def read_config(config_path: str) -> LampGestureConfig:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.load(f)

    return LampGestureConfig(on_gesture=cfg["on_gesture"],
                             off_gesture=cfg["off_gesture"],
                             increase_brightness_gesture=cfg["increase_brightness_gesture"],
                             decrease_brightness_gesture=cfg["decrease_brightness_gesture"])
