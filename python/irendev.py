#!usr/bin/env python
# import RPi.GPIO as GPIO
import time
import evdev
import os
from time import sleep

SWITCH_PLAYLIST = False
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0

D_UP = 2099218
D_DOWN = 2099219
TEN = False


def getTotalQ():
    status = "radio volume: 50%"
    os.system("mpc playlist > tmp")
    status = open("tmp", "r").read()
    tq = status.count("\n") + 1
    global SWITCH_PLAYLIST
    if tq < 10:
        SWITCH_PLAYLIST = True
    print("total queue = " + str(tq))
    return tq


# os.system("mpc volume 50")    
# os.system("ir-keytable -p all")
TOQ = getTotalQ()


def getVol():
    status = "radio volume: 50%"
    os.system("mpc status > tmp")
    status = open("tmp", "r").read()
    # print("s="+status )
    volpos = status.index("volume")
    print(volpos)
    volstatus = status[volpos : volpos + 13]
    print("volstatus=" + volstatus)
    percenpos = volstatus.index("%")
    svol = volstatus[8:percenpos]

    print("svol=" + svol)
    vol = int(svol)

    print("vol=" + str(vol))
    global P_VOL
    P_VOL = vol


def mute():
    getVol()
    print("P_VOL=" + str(P_VOL))
    if P_VOL > 0:
        global C_VOL
        C_VOL = P_VOL
        os.system("mpc volume 0")
    else:
        os.system("mpc volume " + str(C_VOL))


def getPlayState():
    status = "radio volume: 50%"
    os.system("mpc > tmp")
    status = open("tmp", "r").read()
    # volpos = status.index('playing')
    if "playing" in status:
        return True
    else:
        return False

def playToggle():
    if (getPlayState()) is True:
        os.system("mpc stop")
    else:
        os.system("mpc play")

def setVOL(up):
    if (getPlayState()) is True:
        if up is True:
            print("set volume up")
            os.system("mpc volume +5")
        else:
            os.system("mpc volume -5")


def setSTATION(next):
    if (getPlayState()) is True:
        if next is True:
            os.system("mpc next")
        else:
            os.system("mpc prev")


def playPos(pos):
    global TEN
    if TEN is True:
        global TOQ
        if TOQ > 10:
            pos = pos + 10
            os.system("mpc play " + str(pos))
            TEN = False
        else:
            os.system("mpc play " + str(pos))
    else:
        os.system("mpc play " + str(pos))


def switchPLAYLIST():
    global SWITCH_PLAYLIST
    SWITCH_PLAYLIST = not SWITCH_PLAYLIST
    if SWITCH_PLAYLIST is True:
        os.system("mpc clear")
        sleep(0.1)
        os.system("mpc load koplo")
    else:
        os.system("mpc clear")
        sleep(0.1)
        os.system("mpc load radio")


def get_ir_values():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.name)
        if device.name == "sunxi-ir":
            print("Using device", device.path, "\n")
            return device
        print("No device found!")


dev = get_ir_values()
time.sleep(1)
events = dev.read()

try:
    event_list = [event.value for event in events]
    print("Receved command:", event_list)
except BlockingIOError:
    print("No commands received. \n")
NUM_1 = 2099228
NUM_2 = 2099229
NUM_3 = 2099230
NUM_4 = 2099264
NUM_5 = 2099265
NUM_6 = 2099266
NUM_7 = 2099268
NUM_8 = 2099269
NUM_9 = 2099270
NUM_0 = 2099271
NUM_PAD = [2099228 ,2099229 ,2099230 ,2099264 ,2099265 ,2099266 ,2099268 ,2099269 ,2099270 ,2099271]
VOLUP = 2099202
VOLDOWN = 2099203
STUP = 2099206
STDOWN = 2099207
while True:
    event = dev.read_one()
    if event:
        print(event.value)
        hexval = hex(event.value)
        print(hexval)
        # sval=str(event.value)
        irval = event.value
        if irval == 2099218:
            print("UP")
            setVOL(True)
        if event.value == VOLUP:
            print("volume up")
            setVOL(True)
        if event.value == VOLDOWN:
            setVOL(False)
        if event.value == STUP:
            setSTATION(True)
        if event.value == STDOWN:
            setSTATION(False)
        # if event.value== D_UP:
        #     print("dUP")
        #     setVOL(False)
        if irval == 2099219:
            print("DOWN")
            setVOL(False)
        if irval == 2099222:
            print("right")
            setSTATION(True)
        if irval == 2099220:
            print("left")
            setSTATION(False)
        if irval == 2099278:
            print("play")
            os.system("mpc play")
        if irval == 2099277:
            print("stop")
            os.system("mpc stop")
        if irval == 2099204:
            print("mute")
            mute()
        if irval == 2099205:
            print("tv")  # switch playlist
            switchPLAYLIST()
        if irval == 2099214:  # 10+
            print("mai;")
            # global TEN
            TEN = True
        if irval == 2099228:  # 1
            print("")
            playPos(1)
        if irval == 2099229:  # 2
            print("")
            playPos(2)
        if irval == 2099230:  # 3
            print("")
            playPos(3)
        if irval == NUM_4:
            playPos(4)
        if irval == NUM_5:
            playPos(5)
        if irval == NUM_6:
            playPos(6)
        if irval == NUM_7:
            playPos(7)
        if irval == NUM_8:
            playPos(8)
        if irval == NUM_9:
            playPos(9)
        if irval == NUM_0:
            playPos(10)
        # mini remote=========================
            # if irval ==79:
            #     setVOL(True)
            # if event.value == 85:
            #     setVOL(False)
            # if event.value == 89:
            #     setSTATION(True)
            # if event.value == 86:
            #     setSTATION(False)
            # if irval == 36: #playpause
            #     print("play")
            #     os.system("mpc play")
            # if irval == 65:
            #     print("mute")
            #     mute()
            # if irval == 84:
            #     print("tv")  # switch playlist
            #     switchPLAYLIST()
            # if irval == 81:  # 10+
            #     print("call butn")
            #     TEN = True
            # if irval == 12:  # 1
            #     print("")
            #     playPos(1)
            # if irval == 13  :  # 2
            #     print("")
            #     playPos(2)
            # if irval == 14:  # 3
            #     print("")
            #     playPos(3)
            # if irval == 16:
            #     playPos(4)
            # if irval == 17:
            #     playPos(5)
            # if irval == 18:
            #     playPos(6)
            # if irval == 20:
            #     playPos(7)
            # if irval == 32:
            #     playPos(8)
            # if irval == 33:
            #     playPos(9)
            # if irval == 34:
            #     playPos(10)
            # sleep(0.5)
