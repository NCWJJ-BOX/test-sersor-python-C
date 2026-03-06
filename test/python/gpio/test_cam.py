import time

import importlib
from typing import Any

TRIG_PIN = 27
ECHO_PIN = 22
BUTTON_PIN = 18
SERVO_PIN = 4


def load_gpio() -> Any | None:
    try:
        return importlib.import_module("RPi.GPIO")
    except ModuleNotFoundError:
        return None


def load_cv2() -> Any | None:
    try:
        return importlib.import_module("cv2")
    except ModuleNotFoundError:
        return None


def setup_gpio(gpio: Any):
    # Set up GPIO for Ultrasonic sensor
    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG_PIN, gpio.OUT)  # Trig pin for Ultrasonic sensor
    gpio.setup(ECHO_PIN, gpio.IN)  # Echo pin for Ultrasonic sensor
    gpio.setup(BUTTON_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)  # GPIO for camera trigger (Button)

    # Set up GPIO for Servo (if you need to include the servo control)
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

def capture_image(cv2: Any, cam: Any) -> None:
    for i in range(10):
        start_time = time.time()
        ret, image = cam.read()
        end_time = time.time()
        
        time1 = end_time - start_time
        print(f"time : {time1:.4f}")
        
        if not ret:
            print("Not_save_img")
            return
        
        cv2.imwrite("img_" + str(i) + ".jpg", image)
        time_img_save = time.time()
        time2 = time_img_save - start_time
        print(f"time_img : {time2:.4f}")
        print(f"Save_img {i}")

        cv2.destroyAllWindows()

def main():
    gpio = load_gpio()
    if gpio is None:
        print("RPi.GPIO not installed; cannot use GPIO")
        return
    cv2 = load_cv2()
    if cv2 is None:
        print("cv2 not installed; cannot use camera")
        return

    pwm = setup_gpio(gpio)
    print("Starting...")
    cam = cv2.VideoCapture(0)

    try:
        if not cam.isOpened():
            print("Camera not open")
            return

        while True:
            # Measure the distance from the Ultrasonic sensor
            dist = get_distance(gpio)
            print(f"Distance: {dist:.2f} cm")

            if dist < 30:  # If the distance is less than 30 cm
                print("Object detected within 30 cm! Capturing image...")
                capture_image(cv2, cam)  # Call the capture image function
                break  # Exit the loop after capturing the image

            time.sleep(0.1)  # Wait a bit before checking the distance again
    finally:
        pwm.stop()
        gpio.cleanup()  # Clean up GPIO
        cam.release()  # Release the camera

if __name__ == "__main__":
    main()
