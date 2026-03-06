# Test Folder Layout

This folder contains quick hardware/IO test scripts and sample assets.

## Layout

- `test/python/gpio/` - Raspberry Pi GPIO tests (ultrasonic / servo / relay / camera)
- `test/python/serial/` - Serial tests (Raspberry Pi <-> Arduino)
- `test/python/integration/` - Integration tests (serial + camera)
- `test/cpp/` - C++ experiments/tests
- `test/assets/images/samples/` - Sample images committed to the repo
- `test/assets/images/captures/` - Runtime captures (gitignored)

## Python Scripts

### GPIO (`test/python/gpio/`)

- `test_all.py` - Combined GPIO flow (ultrasonic + relay + servo + camera capture)
- `test_cam.py` - Ultrasonic + camera capture script
- `test_relay.py` - Relay on/off loop test
- `test_servo.py` - Ultrasonic-triggered servo movement test
- `test_u.py` - Ultrasonic distance print test
- `test_ultrasonic_and_servo.py` - Ultrasonic + servo combined test

### Serial (`test/python/serial/`)

- `read_distance.py` - Read distance lines from serial and print `Distance: <value> cm`
- `send_hello.py` - Send one `Hello from RPi` message over serial
- `read_0_1.py` - Read and print `0`/`1` values from serial

### Integration (`test/python/integration/`)

- `test_rpi_and_r3.py` - Serial + camera integration with relay/servo commands

## Run Examples

Run from repository root:

```bash
python test/python/serial/read_distance.py
python test/python/serial/send_hello.py
python test/python/serial/read_0_1.py
python test/python/gpio/test_u.py
python test/python/integration/test_rpi_and_r3.py
```

## Notes

- Scripts that use `RPi.GPIO` and/or `cv2` may print a message and exit if those modules are not installed.
- Serial scripts may print a message and exit if `pyserial` is not installed.
- Image capture scripts write new images to `test/assets/images/captures/` by default.
