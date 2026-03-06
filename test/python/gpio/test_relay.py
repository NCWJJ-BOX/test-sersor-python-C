import time

import importlib
from typing import Any

RELAY_PIN = 23


def load_gpio() -> Any | None:
    try:
        return importlib.import_module("RPi.GPIO")
    except ModuleNotFoundError:
        return None

def relay_on(gpio: Any) -> None:
    gpio.output(RELAY_PIN, gpio.HIGH)
    print("Relay ON")

def relay_off(gpio: Any) -> None:
    gpio.output(RELAY_PIN, gpio.LOW)
    print("Relay OFF")

def main() -> None:
    gpio = load_gpio()
    if gpio is None:
        print("RPi.GPIO not installed; cannot use GPIO")
        return

    gpio.setmode(gpio.BCM)
    gpio.setup(RELAY_PIN, gpio.OUT)

    try:
        while True:
            relay_on(gpio)
            time.sleep(2)
            relay_off(gpio)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        gpio.cleanup()


if __name__ == "__main__":
    main()
