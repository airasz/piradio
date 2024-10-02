#!/usr/bin/env python

# Ported from:
# https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont

font = ImageFont.load_default()
device = ssd1306(port=3, address=0x3C)

with canvas(device) as draw:
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
   
    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)

    # Write two lines of text.
    draw.text((0, 0),    'Hello',  fill=2)
    draw.text((0, 20), 'World!',  fill=2)
