import time
import importlib
from pathlib import Path

TRIG_PIN = 27
ECHO_PIN = 22

# Optional input pin (currently unused, but kept to match existing wiring)
BUTTON_PIN = 18

RELAY_PIN = 23
SERVO_PIN = 4

SERVO_PWM_HZ = 50


_cv2_cache = None
_gpio_cache = None


def load_cv2():
    global _cv2_cache
    if _cv2_cache is not None:
        return _cv2_cache
    try:
        _cv2_cache = importlib.import_module("cv2")
    except ModuleNotFoundError:
        _cv2_cache = None
    return _cv2_cache


def load_gpio():
    global _gpio_cache
    if _gpio_cache is not None:
        return _gpio_cache
    try:
        _gpio_cache = importlib.import_module("RPi.GPIO")
    except ModuleNotFoundError:
        _gpio_cache = None
    return _gpio_cache


def setup_gpio(gpio):
    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG_PIN, gpio.OUT)
    gpio.setup(ECHO_PIN, gpio.IN)
    gpio.setup(BUTTON_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.setup(RELAY_PIN, gpio.OUT)
    gpio.setup(SERVO_PIN, gpio.OUT)

    pwm = gpio.PWM(SERVO_PIN, SERVO_PWM_HZ)
    pwm.start(0)
    return pwm


def relay_on(gpio):
    gpio.output(RELAY_PIN, gpio.HIGH)
    print("relay ON")

def relay_off(gpio):
    gpio.output(RELAY_PIN, gpio.LOW)
    print("relay OFF")

def get_distance(gpio, timeout_s=0.03):
    gpio.output(TRIG_PIN, gpio.LOW)
    time.sleep(0.0002)

    gpio.output(TRIG_PIN, gpio.HIGH)
    time.sleep(0.00001)
    gpio.output(TRIG_PIN, gpio.LOW)

    wait_start = time.time()
    while gpio.input(ECHO_PIN) == gpio.LOW:
        if time.time() - wait_start > timeout_s:
            return None

    pulse_start = time.time()
    while gpio.input(ECHO_PIN) == gpio.HIGH:
        if time.time() - pulse_start > timeout_s:
            return None

    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return pulse_duration * 17150

def get_average_distance(gpio, num_samples=3, sample_delay_s=0.05):
    distances = []
    for _ in range(num_samples):
        dist = get_distance(gpio)
        if dist is not None:
            distances.append(dist)
        time.sleep(sample_delay_s)

    if not distances:
        return None

    return sum(distances) / len(distances)

def move_servo(pwm, angle, settle_s=0.5):
    angle = max(0, min(180, int(angle)))
    duty = (angle / 18) + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(settle_s)
    pwm.ChangeDutyCycle(0)

def capture_image(cv2, cam, count=10, filename_prefix="img_"):
    captures_dir = (
        Path(__file__).resolve().parents[3]
        / "assets"
        / "images"
        / "captures"
    )
    captures_dir.mkdir(parents=True, exist_ok=True)
    run_id = str(time.time_ns())

    for i in range(count):
        start_time = time.time()
        ret, image = cam.read()
        end_time = time.time()

        read_time_s = end_time - start_time
        print(f"time : {read_time_s:.4f}")

        if not ret:
            print("Not_save_img")
            return

        filename = captures_dir / f"{filename_prefix}{run_id}_{i}.jpg"
        ok = cv2.imwrite(str(filename), image)
        save_time_s = time.time() - start_time
        print(f"time_img : {save_time_s:.4f}")
        if ok:
            print(f"Save_img {i}")
        else:
            print(f"Failed to save {filename}")

    cv2.destroyAllWindows()

def main():
    gpio = load_gpio()
    if gpio is None:
        print("RPi.GPIO not installed; cannot use GPIO")
        return

    cam = None
    pwm = setup_gpio(gpio)

    try:
        cv2 = load_cv2()
        if cv2 is None:
            print("cv2 not installed; cannot use camera")
            return

        relay_on(gpio)
        move_servo(pwm, 180)
        print("Starting...")

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Camera not open")
            return

        while True:
            avg_dist = get_average_distance(gpio)
            if avg_dist is None:
                print("Distance: timeout")
                time.sleep(0.1)
                continue

            print(f"Distance: {avg_dist:.2f} cm")

            if avg_dist < 28.7 or avg_dist > 34:
                print("Object detected within 29 cm! Capturing image...")
                capture_image(cv2, cam)
                move_servo(pwm, 180)
                time.sleep(1)
                move_servo(pwm, 30)
                time.sleep(1)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        try:
            relay_off(gpio)
        finally:
            if cam is not None:
                cam.release()
            pwm.stop()
            gpio.cleanup()

if __name__ == "__main__":
    main()
