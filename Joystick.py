import os
import time
import math
import subprocess
import spidev
from gpiozero import Button

SPI_BUS = 0
SPI_DEVICE = 0

X_CH = 0
Y_CH = 1
BUTTON_PIN = 22

DEADZONE = 90
MAX_STEP = 25
POLL_DELAY = 0.02

YDOTOOL = "/usr/local/bin/ydotool"
os.environ.setdefault("YDOTOOL_SOCKET", "/tmp/.ydotool_socket")

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1000000

button = Button(BUTTON_PIN, pull_up=True)

last_click_time = 0
click_debounce = 0.25

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 0x03) << 8) | adc[2]

def normalize(value, center=512):
    offset = value - center
    if abs(offset) < DEADZONE:
        return 0.0
    if offset > 0:
        return (offset - DEADZONE) / (1023 - center - DEADZONE)
    return (offset + DEADZONE) / (center - DEADZONE)

def scaled_step(norm):
    if norm == 0:
        return 0
    step = int(math.copysign(max(1, int((abs(norm) ** 1.6) * MAX_STEP)), norm))
    return step

def run_ydotool(args):
    subprocess.run([YDOTOOL] + args, check=False)

try:
    print("Starting joystick mouse control. Press Ctrl+C to stop.")
    while True:
        x_raw = read_adc(X_CH)
        y_raw = read_adc(Y_CH)

        x_norm = normalize(x_raw)
        y_norm = normalize(y_raw)

        dx = scaled_step(x_norm)
        dy = scaled_step(y_norm)

        if dx != 0 or dy != 0:
            run_ydotool(["mousemove_relative", "--", str(dx), str(-dy)])

        now = time.time()
        if button.is_pressed and (now - last_click_time) > click_debounce:
            run_ydotool(["click", "0xC0"])
            last_click_time = now

        time.sleep(POLL_DELAY)

except KeyboardInterrupt:
    print("Stopping.")
finally:
    spi.close()
