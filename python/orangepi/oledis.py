from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT

from pathlib import Path
from PIL import ImageFont
# font25 = ImageFont.truetype(Dejavu, 25)

font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'DejaVuSansMono.ttf'))
font2 = ImageFont.truetype(font_path, 10)
font3 = ImageFont.truetype(font_path, 30)

def do_nothing(obj):
	pass

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial, rotate=2)
device.cleanup = do_nothing

class oled:
	def display(self, msg):
		with canvas(device) as draw:
			draw.text((0, 0), msg, fill="white",font=font2)
		return

	def display(self, msg, cursor):
		with canvas(device) as draw:
			draw.text(cursor, msg, fill="white",font=font2)
		return
	def displaybig(self, msg):
		with canvas(device) as draw:
			draw.text((0, 0), msg, fill="white",font=font3)
		return


	def showmsg(self, msg):
		show_message(device, msg, fill="white", font=font2)
		return

	def clear(self, cmode):
		if cmode == 0:
			device.clear() # clears to display immediately
		elif cmode == 1:
			device.hide() # put the device into low-power sleep, switching the screen off
		#device.show() # wake the device from low-power sleep, which restores the previously displayed value
		return
	def show(self):
		device.show() # wake the device from low-power sleep, which restores the previously displayed value
		return
