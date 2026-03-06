import time

import importlib
from typing import Any

TRIG_PIN = 27
ECHO_PIN = 22
SERVO_PIN = 4


def load_gpio() -> Any | None:
    try:
        return importlib.import_module("RPi.GPIO")
    except ModuleNotFoundError:
        return None


def setup_gpio(gpio: Any):
    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG_PIN, gpio.OUT)  # Trig pin for Ultrasonic sensor
    gpio.setup(ECHO_PIN, gpio.IN)  # Echo pin for Ultrasonic sensor
    gpio.setup(SERVO_PIN, gpio.OUT)  # Servo control pin

    # Setup PWM for servo motor
    pwm = gpio.PWM(SERVO_PIN, 50)  # 50Hz for servo motor
    pwm.start(0)
    return pwm

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

def move_servo(pwm):
    # Move servo from 0 to 180 degrees and back to 0
    for angle in range(0, 181, 10):  # Increase angle from 0 to 180
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    time.sleep(1)  # Hold at 180 degrees

    for angle in range(180, -1, -10):  # Decrease angle from 180 to 0
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    pwm.ChangeDutyCycle(0)  # Stop the servo from moving

def main() -> None:
    gpio = load_gpio()
    if gpio is None:
        print("RPi.GPIO not installed; cannot use GPIO")
        return

    pwm = setup_gpio(gpio)
    try:
        while True:
            dist = get_distance(gpio)
            print(f"Distance: {dist:.2f} cm")

            if dist < 30:
                print("Object detected within 30 cm! Moving servo...")
                move_servo(pwm)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        pwm.stop()
        gpio.cleanup()


if __name__ == "__main__":
    main()



