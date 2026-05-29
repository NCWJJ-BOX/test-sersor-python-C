# Sensor Test Scripts

Quick hardware/IO test scripts for Raspberry Pi GPIO peripherals (ultrasonic, servo, relay, camera) and Arduino serial communication.

## Project Structure

```
test-sersor-python-C/
├── test/
│   ├── python/
│   │   ├── gpio/
│   │   │   ├── test_all.py               # Combined: ultrasonic + relay + servo + camera
│   │   │   ├── test_cam.py               # Ultrasonic-triggered camera capture
│   │   │   ├── test_servo.py             # Ultrasonic-triggered servo sweep
│   │   │   ├── test_relay.py             # Relay on/off loop
│   │   │   ├── test_u.py                 # Ultrasonic distance print
│   │   │   └── test_ultrasonic_and_servo.py
│   │   ├── serial/
│   │   │   ├── read_distance.py          # Read distance from Arduino
│   │   │   ├── send_hello.py             # Send hello to Arduino
│   │   │   └── read_0_1.py               # Read 0/1 values
│   │   └── integration/
│   │       └── test_rpi_and_r3.py        # Full integration: serial + camera + relay + servo
│   ├── cpp/
│   │   ├── r3.cpp                        # Arduino: ultrasonic + servo + serial commands
│   │   ├── test.cpp                      # Arduino: ultrasonic + servo + 0/1 output
│   │   ├── test-r3.cpp                   # Arduino: ultrasonic threshold + servo
│   │   └── test-ultra-infra.cpp          # Arduino: ultrasonic + infrared + servo
│   └── assets/images/samples/            # Sample captured images
└── README.md
```

## Features

- Modular test scripts — each sensor component has standalone test
- GPIO-based ultrasonic distance (BCM: Trig=27, Echo=22)
- PWM servo control with configurable angle
- Relay on/off toggling
- Camera capture with image saving
- Average distance sampling (multi-sample)
- Serial communication with Arduino
- Arduino C++ supports serial command protocol (`relay_on`, `relay_off`, `move_servo <angle>`)

## Tech Stack

- **Python:** RPi.GPIO, pyserial, opencv-python (cv2)
- **C++:** Arduino Servo library
- **Hardware:** HC-SR04, SG90 servo, relay module, infrared sensor, RPi camera

## Usage

### Python GPIO Tests

```bash
python test/python/gpio/test_all.py
python test/python/gpio/test_u.py
python test/python/gpio/test_servo.py
python test/python/gpio/test_relay.py
python test/python/gpio/test_cam.py
```

### Serial Tests

```bash
python test/python/serial/read_distance.py
```

### Integration

```bash
python test/python/integration/test_rpi_and_r3.py
```

### Arduino C++

Upload `.cpp` files via Arduino IDE to target board.

## Hardware Wiring

| Component | Pin |
|-----------|-----|
| HC-SR04 Trig | BCM 27 |
| HC-SR04 Echo | BCM 22 |
| Servo | BCM 17 |
| Relay | BCM 4 |

## Dependencies

- Python: `RPi.GPIO`, `pyserial`, `opencv-python`
- Arduino: `Servo.h`
