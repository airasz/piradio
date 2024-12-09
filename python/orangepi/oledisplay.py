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
font3 = ImageFont.truetype(font_path, 20)

def do_nothing(obj):
	pass

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial, rotate=2)
device.cleanup = do_nothing
matchminute=""
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

	def displayfs(self, msg, font_size):
		cfont = ImageFont.truetype(font_path, font_size)
		with canvas(device) as draw:
			draw.text((0, 0), msg, fill="white",font=cfont)
		return

	def displayfscs(self, msg, font_size, cursor):
		cfont = ImageFont.truetype(font_path, font_size)
		with canvas(device) as draw:
			draw.text(cursor, msg, fill="white",font=cfont)
		return
	def update(self, mnt):
		global matchminute
		matchminute=mnt

	def displayduo(self, msg1, msg2, font_size, cursor1, cursor2):
		cfont = ImageFont.truetype(font_path, font_size)
		global matchminute
		with canvas(device) as draw:
			draw.text(cursor1, msg1, fill="white",font=cfont)
			draw.text(cursor2, msg2, fill="white",font=font2)
			draw.rectangle((34,32,80, 10), fill="black")
			# draw.rectangle((x1,y2,x2, y1), fill="white")
			draw.text((44, 10), matchminute, fill="white",font=font3)
		return
