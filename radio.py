#!usr/bin/python
# requires RPi_I2C_driver.py
#import RPi_I2C_driver
#import lcdui
import os
import OPi.GPIO as GPIO
# from pyA20.gpio import gpio
# from pyA20.gpio import port
from time import sleep
# from apscheduler.scheduler import Scheduler
# set up the pins

# currentvol = 0
#blocking = 0;
muted=False
#pylirc.init("pylirc",  blocking)
sleep(1)

# sleep(.5)

#  vol = open('piRadioSavedVol', 'r')
#  currentvol = int(vol.read())
#  vol.close()
#  mylcd.lcd_display_string_pos("V:", 1, 12)
#  mylcd.lcd_display_string_pos(str(currentvol), 1, 14)

def saveVol():
    global currentvol
    vol = open('vol', 'w')
    vol.write(str(volpercent))
    vol.close()

def saveSts():
    global currentsts
    sts = open('station', 'w')
    sts.write(str(station))
    sts.close()

def loadVol():
    global currentvol
    vol = open('vol', 'r')
    currentvol = int(vol.read())
    volpercent = currentvol
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(str(currentvol), 1, 14)
    vol.close()

def loadSts():
    global currentsts
    sts = open('station', 'r')
    currentsts = int(sts.read())
    percent = currentsts
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(str(currentvol), 1, 14)
    sts.close()

loadVol()
loadSts()
sleep(.5)  # 2 sec delay

# mylcd.lcd_clear()

angka = 0


def counting():
    # import time
    global angka
    while True:
        angka += 1
        sleep(0.5)
        if angka > 60:
            #mylcd.backlight(0)
            angka = 0

# counting()


volpercent = currentvol
# volpercent = 70
volstring = ""
volstring1 = "amixer sset  PCM,0 "
volstring2 = "%"
volume = ""
vol_dir = False


def setvolumeUP():
    global volpercent
    #global station
    #myoled.showstation(station)
    volpercent += 5
    if volpercent > 100:
        volpercent = 100
    volstring = str(volpercent)
    volume = ("mpc volume "+volstring)
    os.system(volume)
    print volume
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(volstring, 1, 14)
    #ui.showvolbar(volpercent)
    volumestr="volume : "
    # myoled.showvolpercent(volumestr +volstring)

def  mute(mute):
    global volpercent
    global tmp_vol
    if mute==True:
        tmp_vol=volpercent
        volpercent=50
        volstring = str(volpercent)
        volume = (volstring1 + volstring + volstring2)
        os.system(volume)
        myoled.settext(3, "Muted")
    else:
        #loadVol()
        sleep(.2)
        volpercent=tmp_vol
        volstring = str(volpercent)
        volume = (volstring1 + volstring + volstring2)
        volumestr="volume : "
        os.system(volume)
        myoled.showvolpercent(volumestr +volstring)
        
def setvolumeDOWN():
    global volpercent
    #global station
    #myoled.showstation(station)
    volpercent -= 5
    if volpercent < 0:
        volpercent = 0
    volstring = str(volpercent)
    volume = ("mpc volume "+volstring)
    os.system(volume)
    print volume
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(volstring, 1, 14)
    #ui.showvolbar(volpercent)    
    volumestr="volume : "
    # myoled.showvolpercent(volumestr +volstring)


# os.system("piradio")
# os.system("amixer sset  PCM,0 70%")
volstring = str(volpercent)
os.system("mpc volume "+volstring)
print (volstring1 + volstring + volstring2)
station = 0
volume = 9
count_s_mode = 1
radio_mode = 1


def pickstationUP():
    global station
    global rpwr
    global radio_mode
    #  if station == 0:
            # loadVol()
    station += 1
    rpwr = True
    # print station
    #ui.showstation(station)

    os.system("mpc play "+ str(station))
    # myoled.showstation(station)

    return


def pickstationDOWN():
    global station
    global rpwr
    if station == 9:
        os.system("vlc vlc://quit")
        sleep(1)
    station -= 1
    if station < 0
        station = 9
    rpwr = True
    # print station
    
    #ui.showstation(station)

    return


rpwr = True


def power():
    global rpwr
    global station
    if rpwr is False:
        rpwr = True
        os.system("mpc play " str(station))
        print "piradio on"
        myoled.showstation(station)
    else:
        rpwr = False
        # os.system("sudo killall -9 mpd")
        os.system("mpc stop")
        print "piradio off"
        # myoled.settext(1, "Raspberry pi")
        # myoled.settext(2, "Internet Radio")
        # myoled.settext(3, "Stopped")
