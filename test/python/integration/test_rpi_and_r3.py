import time

import importlib
from typing import Any


SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600
TIMEOUT_S = 1


def load_serial() -> Any | None:
    try:
        return importlib.import_module("serial")
    except ModuleNotFoundError:
        return None


def load_cv2() -> Any | None:
    try:
        return importlib.import_module("cv2")
    except ModuleNotFoundError:
        return None


def reinitialize_arduino(serial: Any) -> Any | None:
    SerialException = getattr(serial, "SerialException", Exception)
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT_S)
        time.sleep(3)
        print("Reinitialized Arduino connection")
        return arduino
    except SerialException as e:
        print(f"Failed to reinitialize Arduino: {e}")
        return None


def safe_arduino_write(serial: Any, arduino: Any | None, command: bytes) -> Any | None:
    if arduino is None:
        return None

    SerialException = getattr(serial, "SerialException", Exception)
    try:
        _ = arduino.write(command)
        arduino.flush()
        return arduino
    except SerialException as e:
        print(f"Error during serial communication: {e}")
        arduino.close()
        time.sleep(2)
        return reinitialize_arduino(serial)

def relay_on(serial: Any, arduino: Any | None) -> Any | None:
    print("Turning relay ON...")
    return safe_arduino_write(serial, arduino, b"relay_on\n")

def relay_off(serial: Any, arduino: Any | None) -> Any | None:
    print("Turning relay OFF...")
    return safe_arduino_write(serial, arduino, b"relay_off\n")

def move_servo(serial: Any, arduino: Any | None, angle: float) -> Any | None:
    if arduino is None:
        return None

    SerialException = getattr(serial, "SerialException", Exception)
    try:
        _ = arduino.write(f"move_servo {angle}\n".encode())
        arduino.flush()
        print(f"Moving servo to {angle} degrees")
        return arduino
    except SerialException as e:
        print(f"Error while moving servo: {e}")
        return arduino

def capture_image(cv2: Any, cam: Any) -> None:
    for i in range(5):
        start_time = time.time()
        ret, image = cam.read()  
        end_time = time.time()

        if not ret:
            print("Not_save_img") 
            return

        filename = f"img_{i}.jpg"
        cv2.imwrite(filename, image) 
        print(f"Saved {filename}")

    cv2.destroyAllWindows()

def read_distance_from_arduino(serial: Any, arduino: Any | None) -> tuple[str | None, Any | None]:
    if arduino is None:
        return None, None

    SerialException = getattr(serial, "SerialException", Exception)
    try:
        if arduino.in_waiting > 0:
            distance = arduino.readline().decode("utf-8", errors="ignore").strip()
            if distance == "READY":
                return "READY", arduino  # Indicates Arduino is ready for the next task
            return distance, arduino
        return None, arduino
    except SerialException as e:
        print(f"Error while reading data: {e}")
        return None, reinitialize_arduino(serial)

def main():
    serial = load_serial()
    if serial is None:
        print("pyserial not installed; cannot use serial")
        return

    cv2 = load_cv2()
    if cv2 is None:
        print("cv2 not installed; cannot use camera")
        return

    arduino = reinitialize_arduino(serial)
    if arduino is None:
        print("Failed to initialize Arduino. Exiting...")
        return

    arduino = relay_on(serial, arduino)
    print("Starting...")

    cam = cv2.VideoCapture(0)

    try:
        if not cam.isOpened():
            print("Camera not open")
            return

        while True:
            distance, arduino = read_distance_from_arduino(serial, arduino)

            if distance:
                print(f"Distance: {distance} cm")

                if distance == "READY":
                    print("Arduino is ready for the next operation.")
                    continue  # Wait for Arduino to be ready for the next operation

                if "Distance:" in distance:
                    distance = distance.replace("Distance:", "").strip()

                try:
                    distance_value = float(distance)
                    if distance_value < 27.5 or distance_value > 32:
                        print("Capturing image...")
                        capture_image(cv2, cam)
                        arduino = move_servo(serial, arduino, 50)
                        time.sleep(2)
                except ValueError:
                    print(f"Invalid distance value received: {distance}. Skipping...")
            
            time.sleep(0.1)  # Wait a little before checking the distance again

    finally:
        arduino = relay_off(serial, arduino)
        cam.release()
        if arduino is not None:
            arduino.close()

if __name__ == "__main__":
    main()
    
