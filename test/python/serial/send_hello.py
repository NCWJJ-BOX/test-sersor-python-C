import time

import importlib
from typing import Any


SERIAL_PORT = "/dev/ttyUSB0"  # แทนที่ '/dev/ttyUSB0' ด้วยพอร์ตที่ใช้งานจริง
BAUD_RATE = 9600


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

    # กำหนดพอร์ตที่เชื่อมต่อกับ Arduino
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)

    try:
        time.sleep(2)  # รอให้ Arduino เริ่มทำงาน

        # ส่งข้อมูลไปยัง Arduino
        _ = arduino.write(b"Hello from RPi\n")
    finally:
        # ปิดการเชื่อมต่อ
        arduino.close()


if __name__ == "__main__":
    main()
