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


def main() -> None:
    serial = load_serial()
    if serial is None:
        print("pyserial not installed; cannot use serial")
        return

    # เชื่อมต่อกับพอร์ตที่ Arduino ใช้
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT_S)

    # รอให้การเชื่อมต่อกับ Arduino พร้อม
    time.sleep(2)

    try:
        while True:
            # อ่านค่าจาก Serial
            if arduino.in_waiting > 0:
                distance = arduino.readline().decode("utf-8").strip()
                print(f"Distance: {distance} cm")

            time.sleep(1)
    finally:
        arduino.close()


if __name__ == "__main__":
    main()
