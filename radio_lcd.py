#!usr/bin/python
# requires RPi_I2C_driver.py
#import RPi_I2C_driver
#import lcdui
import lirc
import Adafruit_SSD1306
import oledUI
import os
import RPi.GPIO as GPIO
from time import sleep
# from apscheduler.scheduler import Scheduler
# set up the pins

# currentvol = 0
#blocking = 0;
muted=False
#pylirc.init("pylirc",  blocking)
sleep(1)
try:
    sockid=lirc.init("radio_lcd", blocking=False)
except:
    print ("lirc cannot init")
# import subprocess
GPIO.setmode(GPIO.BCM)
# GPIO.setup(21,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(4, GPIO.IN)

#mylcd = RPi_I2C_driver.lcd()
myoled= oledUI.oled()
#ui=lcdui.show(()
#ui=oledUI.show()
# scheduler
# schd=Scheduler()

# test 2
#mylcd.lcd_display_string("RPi ", 1)
#mylcd.lcd_display_string("Internet Radio", 2)
myoled.settext(1, "raspberry pi")
myoled.settext(2, "Internet Radio")
myoled.settext(3, "by airasz")
os.system("amixer cset numid=3 2")      # 2 is force to HDMI OUTPUT   1 analog
sleep(.5)

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


def loadVol():
    global currentvol
    vol = open('vol', 'r')
    currentvol = int(vol.read())
    volpercent = currentvol
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(str(currentvol), 1, 14)
    vol.close()

loadVol()

sleep(.5)  # 2 sec delay

# mylcd.lcd_clear()

#angka = 0


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
    volpercent += 2
    if volpercent > 100:
        volpercent = 100
    volstring = str(volpercent)
    volume = (volstring1 + volstring + volstring2)
    try:
        os.system(volume)
    except:
        print("cannot set volume")
    print volume
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(volstring, 1, 14)
    #ui.showvolbar(volpercent)
    volumestr="volume : "
    myoled.showvolpercent(volumestr +volstring)

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
    volpercent -= 2
    if volpercent < 0:
        volpercent = 0
    volstring = str(volpercent)
    volume = (volstring1 + volstring + volstring2)
    os.system(volume)
    print volume
    #mylcd.lcd_display_string_pos("V:", 1, 12)
    #mylcd.lcd_display_string_pos(volstring, 1, 14)
    #ui.showvolbar(volpercent)    
    volumestr="volume : "
    myoled.showvolpercent(volumestr +volstring)


# os.system("piradio")
# os.system("amixer sset  PCM,0 70%")
volstring = str(volpercent)
os.system(volstring1 + volstring + volstring2)
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
    if station == 9:
        os.system("vlc vlc://quit")
        sleep(1)
    station += 1
    rpwr = True
    # print station
    #ui.showstation(station)
    if station == 1:
        # global volpercent
        # loadVol()
        os.system("piradio rodjaLOW")
        print "play rodja LQ"

    if station == 3:
        os.system("piradio muslim")
        print "play muslim"

    if station == 8:
        os.system("piradio insani")
        print "play Insani"

    if station == 4:
        #os.system("amixer sset  PCM,0 74%")
        os.system("piradio annashihah1")
        print "play annasihah1"

    if station == 5:
        os.system("piradio aliman")
        print "play aliman"

    if station == 42:
        os.system("piradio annashihah2")
        print "play annasihah2"
       # mylcd.lcd_clear()
        #mylcd.lcd_display_string("Playing", 1)
        #mylcd.lcd_display_string("Radio annashihah2", 2)

    if station == 6:
        os.system("piradio idza")
        print "play idza'atul khair"

    if station == 88:
        os.system("piradio rodjaLOW")
        print "play rodja LOW"

    if station == 2:
        #os.system("amixer sset  PCM,0 74%")
        os.system("piradio rayfm")
        print "play ray FM"

    if station == 7:
        os.system("piradio cirebon")
        print "rdio kita crebon"

    if station == 19:
        os.system("piradio cirebon")
        print "rdio kita crebon"

    if station == 9:
        os.system("vlc --intf dummy http://audio.rodja.tv:1010/;stream.mp3")
        print "audio rodjaTV"

    if station == 21:
        os.system("piradio radioquran")
        print "radio qur'an 1"

    if station == 22:
        os.system("piradio qcoran")
        print "radio qur'an 2"

    if station == 23:
        os.system("piradio quranradio")
        print "radio qur'an 3"

    if station == 24:
        os.system("piradio coranweb")
        print "radio qur'an 4"

    if (radio_mode == 1) and (station > 9):
        station = 1

    if (radio_mode == 2) and (station > 24):
        station = 21
        
    myoled.showstation(station)

    return


def pickstationDOWN():
    global station
    global rpwr
    if station == 9:
        os.system("vlc vlc://quit")
        sleep(1)
    station -= 1
    rpwr = True
    # print station
    
    #ui.showstation(station)
    if station == 1:
        os.system("piradio rodjaLOW")
        print "play rodja"

    if station == 3:
        os.system("piradio muslim")
        print "play muslim"

    if station == 8:
        os.system("piradio insani")
        print "play Insani"

    if station == 4:
        #os.system("amixer sset  PCM,0 74%")
        os.system("piradio annashihah1")
        print "play annasihah1"

    if station == 5:
        os.system("piradio aliman")
        print "play aliman"

    if station == 55:
        os.system("piradio annashihah2")
        print "play annasihah2"
        #mylcd.lcd_clear()
        #mylcd.lcd_display_string("Playing", 1)
        #mylcd.lcd_display_string("Radio annashihah2", 2)

    if station == 6:
        os.system("piradio idza")
        print "play idza'atul khair"

    if station == 17:
        os.system("piradio rodjaLOW")
        print "play rodja LOW"

    if station == 2:
        #os.system("amixer sset  PCM,0 74%")
        os.system("piradio rayfm")
        print "play ray FM"

    if station == 7:
        os.system("piradio cirebon")
        print "rdio kita crebon"

    if station == 9:
        os.system("vlc --intf dummy http://audio.rodja.tv:1010/;stream.mp3")
        print "audio rodjatv"

    if station == 21:
        os.system("piradio radioquran")
        print "radio qur'an 1"

    if station == 22:
        os.system("piradio qcoran")
        print "radio qur'an 2"

    if station == 23:
        os.system("piradio quranradio")
        print "radio qur'an 3"

    if station == 24:
        os.system("piradio coranweb")
        print "radio qur'an 4"

    if (radio_mode == 1) and (station < 1):
        station = 9

    if (radio_mode == 2) and (station < 21):
        station = 24
    
    myoled.showstation(station)

    return


rpwr = True

def power():
    global rpwr
    global station
    if rpwr is False:
        rpwr = True
        os.system("piradio on")
        print "piradio on"
        myoled.showstation(station)
    else:
        rpwr = False
#        os.system("piradio off")
        os.system("sudo killall -9 mpd")
        print "piradio off"
        #mylcd.lcd_clear()
        #mylcd.lcd_display_string("radio stopped", 1)
        myoled.settext(1, "Raspberry pi")
        myoled.settext(2, "Internet Radio")
        myoled.settext(3, "Stopped")


def ir_listener():
        global station
        global radio_mode
        global muted
        s=lirc.nextcode()
        if s!=[]:
            print s
            if s[0]=="KEY_RIGHT":
                if station > 0:
                    # os.system("piradio off")
                    os.system("sudo killall -9 mpd")
                    print "key up remote pressed"
                sleep(0.2)
                pickstationUP()
            if s[0]=="KEY_LEFT":
                if station > 0:
                    # os.system("piradio off")
                    os.system("sudo killall -9 mpd")
                    print "key up remote pressed"
                sleep(0.2)
                pickstationDOWN()
            if s[0]=="KEY_UP":
                setvolumeUP()
                saveVol()
                sleep(0.2)
            if s[0]=="KEY_DOWN":  
                setvolumeDOWN()
                saveVol()
                sleep(0.2)
            if s[0]=="KEY_POWER":
                myoled.wipe()
                myoled.settext(1,"restarting device")
                sleep(1)                      
                os.system("sudo reboot")
                sleep(0.2)
            if s[0]=="KEY_MUTE":                      
                if muted==False:
                    muted=True
                    mute(True)
                else:
                    muted=False
                    mute(False)
                sleep(0.2)
            if s[0]=="KEY_102ND":
                if station > 0:
                    # os.system("piradio off")
                    os.system("sudo killall -9 mpd")
                if radio_mode == 1:
                    radio_mode = 2
                    station = 21
                else:
                    radio_mode = 1
                    station = 1
                pickstationUP()
                sleep(0.1)
            if s[0]=="KEY_PLAY":
                    power()
                    sleep(.2)


try:
    while True:
        ir_listener()
        if GPIO.input(21):
            angka = 0
            if station > 0:
                if station!=9:
                    os.system("sudo killall -9 mpd")
            sleep(0.2)
            pickstationDOWN()
        if GPIO.input(20):
            angka = 0
            if station > 0:
                if station!=9:
                    os.system("sudo killall -9 mpd")
            sleep(0.2)
            pickstationUP()
        if GPIO.input(17):
           # mylcd.backlight(1)
            angka = 0
            # print "GPIO 26 HIGH"
            power()
            sleep(0.2)
        if GPIO.input(19):    # volume -
            #mylcd.backlight(1)
            angka = 0
            print "GPIO 19 HIGH"
            setvolumeDOWN()
            saveVol()
            sleep(0.2)
        if GPIO.input(16):
            #mylcd.backlight(1)
            angka = 0
            print "GPIO 16 HIGH"
            setvolumeUP()
            saveVol()
            sleep(0.2)
        if GPIO.input(4):
            #mylcd.backlight(1)
            angka = 0
            print "GPIO 4 HIGH"
            if station > 0:
                os.system("sudo killall -9 mpd")
            if radio_mode == 1:
                radio_mode = 2
                station = 21
            else:
                radio_mode = 1
                station = 1
            pickstationUP()
            sleep(0.1)
        else:
            sleep(0.1)
finally:
    GPIO.cleanup()
