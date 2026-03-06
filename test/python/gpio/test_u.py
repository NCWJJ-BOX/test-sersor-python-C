import time

import importlib
from typing import Any

TRIG_PIN = 27
ECHO_PIN = 22


def load_gpio() -> Any | None:
    try:
        return importlib.import_module("RPi.GPIO")
    except ModuleNotFoundError:
        return None

def get_distance(gpio: Any) -> float:
    # Send a pulse to the trig pin
    gpio.output(TRIG_PIN, gpio.LOW)
    time.sleep(0.1)
    gpio.output(TRIG_PIN, gpio.HIGH)
    time.sleep(0.00001)
    gpio.output(TRIG_PIN, gpio.LOW)

    # Wait for the Echo pin to go HIGH and start timing
    pulse_start = time.time()
    while gpio.input(ECHO_PIN) == gpio.LOW:
        pulse_start = time.time()

    # Wait for Echo to go LOW and stop timing
    pulse_end = pulse_start
    while gpio.input(ECHO_PIN) == gpio.HIGH:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance (speed of sound = 34300 cm/s)
    distance = pulse_duration * 17150  # Divide by 2 (round-trip) and convert to cm

    return distance

def main() -> None:
    gpio = load_gpio()
    if gpio is None:
        print("RPi.GPIO not installed; cannot use GPIO")
        return

    # Set up GPIO
    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG_PIN, gpio.OUT)  # Trig pin
    gpio.setup(ECHO_PIN, gpio.IN)  # Echo pin

    try:
        while True:
            dist = get_distance(gpio)
            print(f"Distance: {dist:.2f} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        gpio.cleanup()


if __name__ == "__main__":
    main()
