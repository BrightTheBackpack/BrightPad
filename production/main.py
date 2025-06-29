import board
import digitalio

import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

import time
# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner, DiodeOrientation, MatrixScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.extensions.media_keys import MediaKeys
from kmk.handlers.sequences import simple_key_sequence
from kmk.handlers.keyhandlers import simple_key_handler
from kmk.extensions.RGB import RGB

# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# Add the macro extension
macros = Macros()
layers = Layers()
rgb = RGB(pixel_pin=board.GP26, num_pixels=9,
    rgb_order=(1, 0, 2),  
    hue_default=128,
    sat_default=255,
    val_default=128
)
keyboard.modules.append(macros)
keyboard.extensions.append(MediaKeys())
keyboard.modules.append(layers)
keyboard.extensions.append(rgb)

#display stuff
displayio.release_displays()
i2c = busio.I2C(scl=board.GP7, sda=board.GP6)  # Adjust pins if needed

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 32
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()
display.show(splash)
clock_label = label.Label(terminalio.FONT, text="Starting...", x=10, y=15)
splash.append(clock_label)
hour = 12
minute = 0
second = 0
last_tick = time.monotonic()


keyboard.matrix = MatrixScanner(
    cols=[board.GP0, board.GP2, board.GP1],
    rows=[board.GP27, board.GP28, board.GP29]
)
# Here you define the buttons corresponding to the pins
# Look here for keycodes: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
# And here for macros: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md
MO = KC.MO
keyboard.keymap = [
    [  # Layer 0
        KC.MUTE,     KC.VOLD,     KC.VOLU,
        KC.MPRV,     KC.MPLY,     KC.MNXT,
        KC.RGB_TOG,      MO(1),       simple_key_sequence("test")
    ],
    ]
def update_clock_display(keyboard):
    global last_tick, hour, minute, second
    now = time.monotonic()
    if now - last_tick >= 1.0:
        last_tick = now
        second += 1
        if second >= 60:
            second = 0
            minute += 1
        if minute >= 60:
            minute = 0
            hour += 1
        if hour >= 24:
            hour = 0
        clock_label.text = f"{hour:02}:{minute:02}:{second:02}"

keyboard.after_matrix_scan = update_clock_display

# Start kmk!
if __name__ == '__main__':
    keyboard.go()
