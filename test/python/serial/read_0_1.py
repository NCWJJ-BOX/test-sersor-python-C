import time

import importlib
from typing import Any


# กำหนดพอร์ตและความเร็ว Baud rate ให้ตรงกับ Arduino
# ทั่วไปใน RPi จะเป็น '/dev/ttyUSB0' หรือ '/dev/ttyACM0'
SERIAL_PORT = "/dev/ttyACM0"  # อาจต้องเปลี่ยนตามพอร์ตที่ใช้จริง
BAUD_RATE = 9600  # ต้องตรงกับ Serial.begin(9600) ใน Arduino
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

    SerialException = getattr(serial, "SerialException", Exception)
    try:
        # สร้าง object สำหรับ serial communication
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT_S)

        # รอให้การเชื่อมต่อเสถียร
        time.sleep(2)
        print("Connected to Arduino successfully")

        try:
            while True:
                # อ่านข้อมูลจาก serial
                if ser.in_waiting > 0:  # ตรวจสอบว่ามีข้อมูลรออยู่หรือไม่
                    data = ser.readline().decode("utf-8").strip()  # อ่านและแปลงเป็น string

                    # ตรวจสอบข้อมูลที่ได้รับ
                    if data == "1":
                        print("1")
                    elif data == "0":
                        print("0")
                    else:
                        print(f"Received unexpected data: {data}")

                time.sleep(0.1)  # delay เล็กน้อยเพื่อไม่ให้ CPU ทำงานหนักเกิน
        except KeyboardInterrupt:
            print("\nProgram terminated by user")
        finally:
            ser.close()  # ปิดการเชื่อมต่อ serial
            print("Serial connection closed")
    except SerialException as e:
        print(f"Serial error: {e}")


if __name__ == "__main__":
    main()
