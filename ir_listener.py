#!usr/bin/python
# requires RPi_I2C_driver.py
#import RPi_I2C_driver
#import lcdui
import lirc
import os
from time import sleep
sleep(1)
try:
    sockid=lirc.init("ir_listener")
except:
    print ("lirc cannot init")
try:
    sockid=lirc.init("ir_listener", "lircrc")
except:
    print  ("lirc cannot init2")
try:
    sockid=lirc.init("ir_listener", verbose=True)
except:
    print  ("lirc cannot init2")

def ir_listener():
        s=lirc.nextcode()
        if s!=[]:
            if s[0]=="KEY_RIGHT":
                    # os.system("piradio off")
                print ("key right remote pressed")
                sleep(0.2)
                pickstationUP()
            if s[0]=="KEY_LEFT":
                    # os.system("piradio off")
                # os.system("sudo killall -9 mpd")
                print ("key left remote pressed")
                sleep(0.2)
                pickstationDOWN()
            # if s[0]=="KEY_UP":
            #     setvolumeUP()
            #     saveVol()
            #     sleep(0.2)
            # if s[0]=="KEY_DOWN":  
            #     setvolumeDOWN()
            #     saveVol()
            #     sleep(0.2)
            # if s[0]=="KEY_POWER":
            #     myoled.wipe()
            #     myoled.settext(1,"restarting device")
            #     sleep(1)                      
            #     os.system("mpc stop")
            #     sleep(0.2)
            # if s[0]=="KEY_MUTE":    
            #     os.system("mpc stop")
            #     sleep(0.2)
            # if s[0]=="KEY_102ND":
            #     if station > 0:
            #         # os.system("piradio off")
            #         os.system("sudo killall -9 mpd")
            #     if radio_mode == 1:
            #         radio_mode = 2
            #         station = 21
            #     else:
            #         radio_mode = 1
            #         station = 1
            #     pickstationUP()
            #     sleep(0.1)
            # if s[0]=="KEY_PLAY":
            #         power()
            #         sleep(.2)
try:
    while True:
        ir_listener()
finally:        
    print ("finis")