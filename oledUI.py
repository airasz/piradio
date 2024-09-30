 
import Adafruit_SSD1306


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from time import sleep

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
#draw.rectangle((0,0,20,20),outline=0,fill=255)
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()


class oled:
    def showvolpercent(self, vol):
            #draw.text((x,(width-8)), vol, font=font, fill=255)
            draw.rectangle((0,top+20,width,30), outline=0, fill=0)
            #draw.text((x,top+25), "           ", font=font, fill=255)
            disp.image(image)
            sleep(.1)
            draw.text((x,top+20), vol, font=font, fill=255)
            disp.image(image)   
            disp.display()
            
            return
    def wipe(self):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)   
        disp.display()
       # disp.clear()

        return
    
    def settext(self, line, string):
       
        
        #draw.rectangle((0,0,width,height), outline=0, fill=0)
        if line==1:
            draw.rectangle((0,0,width,10), outline=0, fill=0)
            draw.text((x,top), string, font=font, fill=255)
        if line==2:
            draw.rectangle((0,10,width,20), outline=0, fill=0)
            draw.text((x,top+10), string, font=font, fill=255)
        if line==3:
            draw.rectangle((0,20,width,30), outline=0, fill=0)
            draw.text((x,top+20), string, font=font, fill=255)
        if line==4:
            draw.rectangle((0,32,width,height), outline=0, fill=0)
            draw.text((x,top+25), string, font=font, fill=255)

        disp.image(image)   
        disp.display()
       # disp.clear()

        return
        
    def showstation(self , s):
       # lcd.lcd_display_string("Playing", 1)
        #lcd.lcd_display_string("                ", 2)
        #settext(1, "Playing")
        disp.clear()
        draw.rectangle((0,0,width,top+30), outline=0, fill=0)
        #disp.image(image)
        #disp.display()
        draw.text((x,top), "Now Playing", font=font, fill=255)
        draw.text((x,top+10), "          ", font=font, fill=255)
        #settext(2, "             ") 
        
        if s == 1:           
#            draw.text((x,top), "Radio Rodja LQ", font=font, fill=255)
#            lcd.lcd_display_string("Radio Rodja LQ", 2)
            #settext(2, "Radio Rodja LQ")
             draw.text((x,top+10), "Radio Rodja LQ", font=font, fill=255)
        if s == 2:
#            lcd.lcd_display_string("Radio ray FM", 2)
           # settext(2, "Radio ray FM") 
             draw.text((x,top+10), "Radio ray FM", font=font, fill=255)
        if s == 3:
             draw.text((x,top+10), "Radio muslim", font=font, fill=255)
        if s == 4:
             draw.text((x,top+10), "Radio annasihah", font=font, fill=255)
        if s == 5:
             draw.text((x,top+10), "Radio al-iman", font=font, fill=255)
        if s == 6:
             draw.text((x,top+10), "Idza'atul Khair", font=font, fill=255)
        if s == 7:
             draw.text((x,top+10), "Radio Kita Cirebon", font=font, fill=255)
        if s == 8:
             draw.text((x,top+10), "Radio Insani FM", font=font, fill=255)
        if s == 9:
             draw.text((x,top+10), "Audio rodjaTV", font=font, fill=255)
        if s == 21:
             draw.text((x,top+10), "Radio Quran 1", font=font, fill=255)
        if s == 22:
             draw.text((x,top+10), "Radio Quran 2", font=font, fill=255)
        if s == 23:
             draw.text((x,top+10), "Radio Quran 3", font=font, fill=255)
        if s == 24:
             draw.text((x,to  p+10), "Radio Quran 4", font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        

        return
