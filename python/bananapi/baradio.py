#!usr/bin/env python
# import RPi.GPIO as GPIO
import time
import evdev
# from evdev import InputDevice, categorize, ecodes
import os
from time import sleep


import asyncio
from evdev import InputDevice

SWITCH_PLAYLIST = False
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0

#remot key nexmedia
KR_POWER = 2099200
KR_OPT = 2099287
KR_D_UP = 2099218
KR_D_DOWN = 2099219
KR_VOLUP = 2099202
KR_VOLDOWN = 2099203
KR_STUP = 2099206
KR_STDOWN = 2099207
KR_NUMKEYS=[[1 , 2099228],[2 , 2099229],[3 , 2099230],[4 , 2099264],[5 , 2099265],[6 , 2099266],[7 , 2099268],[8 , 2099269],[9 , 2099270],[10 , 2099271]]

#temporary flag
TEN = False
NUM_VOL=0
TO_REBOOT= False

def getTotalQ():
    status = "radio volume: 50%"
    os.system("mpc playlist > tmp")
    status = open("tmp", "r").read()
    tq = status.count("\n") + 1
    global SWITCH_PLAYLIST

    if "muslim" in status:
        SWITCH_PLAYLIST = False
    # if tq < 10:
    #     SWITCH_PLAYLIST = True
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
        os.system("mpc "+ ("stop" if getPlayState() else "play"))
        os.system("mpc stop")
    else:
        os.system("mpc play")

def setVOL(up):
    if (getPlayState()) is True:
        os.system("mpc "+ ("volume +5" if up else "volume -5"))
        # if up is True:
        #     print("set volume up")
        #     os.system("mpc volume +5")
        # else:
        #     os.system("mpc volume -5")

def setSTATION(next):
    if (getPlayState()) is True:
        os.system("mpc "+ ("next" if next else "prev"))

def reboot():
    global TO_REBOOT
    if TO_REBOOT is False:
        TO_REBOOT = True
    else:
        os.system("reboot")

VOLTO=0
def playPos(pos):
    global TEN
    global VOLTO
    global NUM_VOL
    if TEN is True:
        global TOQ
        if TOQ > 10:
            pos = pos + 10
            os.system("mpc play " + str(pos))
            TEN = False
        else:
            os.system("mpc play " + str(pos))

    else:
        if NUM_VOL == 1:
            VOLTO=pos * 10
            print("start vol========== "+ str(VOLTO))
            NUM_VOL =2
        elif NUM_VOL == 2:
            VOLTO+= pos
            NUM_VOL=0
            os.system("mpc volume " + str(VOLTO))
        else:
            os.system("mpc play " + str(pos))

def startVol():
    global NUM_VOL
    global TEN
    if TEN is True:
        TEN =False
    NUM_VOL=1

def startTenPos():
    global TEN
    global NUM_VOL
    TEN = True
    if NUM_VOL !=0:
        NUM_VOL=0


def switchPLAYLIST():
    global SWITCH_PLAYLIST
    SWITCH_PLAYLIST = not SWITCH_PLAYLIST
    status = os.popen("ls /var/lib/mpd/playlists/").read()
    status = status.replace(".m3u", "")
    starr = status.split("\n")

    length = len(starr)
    for i in range(length - 1):
        print(starr[i])

    os.system("mpc clear")
    sleep(0.1)
    os.system("mpc load " + (str(starr[0]) if SWITCH_PLAYLIST else str(starr[1])))
    os.system("mpc play")
    # if SWITCH_PLAYLIST is True:
    #     os.system("mpc clear")
    #     sleep(0.1)
    #     os.system("mpc load koplo")
    # else:
    #     os.system("mpc clear")
    #     sleep(0.1)
    #     os.system("mpc load radio")

def get_ir_values():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.name)
        if device.name == "sunxi-ir":
            print("Using device", device.path, "\n")
            return device
        # print("No device found!")

dev = get_ir_values()
time.sleep(1)
events = dev.read()
#
# try:
#     event_list = [event.value for event in events]
#     print("Receved command:", event_list)
# except BlockingIOError:
#     print("No commands received. \n")


# dev = InputDevice('/dev/input/event1')

async def main(dev):
        async for ev in dev.async_read_loop():
            # print(repr(ev))
            # print(ev.value)
            if ev:
                irval = ev.value
                print(irval)
                hexval = hex(irval)
                print(hexval)
                # sval=str(irval)

                for i in range(len(KR_NUMKEYS)):
                    # NKV=int(KR_NUMKEYS[i][1])
                    # NKI=int (KR_NUMKEYS[i][0])
                    if irval == KR_NUMKEYS[i][1]:
                        playPos(KR_NUMKEYS[i][0])
                        break
                if irval == 2099218:
                    print("UP")
                    setVOL(True)
                elif irval == KR_VOLUP:
                    print("volume up")
                    setVOL(True)
                elif irval == KR_VOLDOWN:
                    setVOL(False)
                elif irval == KR_STUP:
                    setSTATION(True)
                elif irval == KR_STDOWN:
                    setSTATION(False)
                # elif irval== KR_D_UP:
                #     print("dUP")
                #     setVOL(False)
                elif irval == 2099219:
                    print("DOWN")
                    setVOL(False)
                elif irval == 2099222:
                    print("right")
                    setSTATION(True)
                elif irval == 2099220:
                    print("left")
                    setSTATION(False)
                elif irval == 2099278:
                    print("play")
                    os.system("mpc play")
                elif irval == 2099277:
                    print("stop")
                    os.system("mpc stop")
                elif irval == 2099204:
                    print("mute")
                    mute()
                elif irval == 2099205:
                    print("tv")  # switch playlist
                    switchPLAYLIST()
                elif irval == KR_OPT:
                    print("opt")  # start vol
                    startVol()
                elif irval == 2099214:  # 10+
                    print("mail")
                    startTenPos()
                elif irval == KR_POWER:  # 10+
                    print("reboot")
                    reboot()

asyncio.run(main(dev))





# while True:
#     event = dev.read_one()
#     if event:
#         print(event.value)
#         hexval = hex(event.value)
#         print(hexval)
#         # sval=str(event.value)
#         irval = event.value
#
#         for i in range(len(KR_NUMKEYS)):
#             # NKV=int(KR_NUMKEYS[i][1])
#             # NKI=int (KR_NUMKEYS[i][0])
#             if irval == KR_NUMKEYS[i][1]:
#                 playPos(KR_NUMKEYS[i][0])
#                 break
#         if irval == 2099218:
#             print("UP")
#             setVOL(True)
#         elif event.value == KR_VOLUP:
#             print("volume up")
#             setVOL(True)
#         elif event.value == KR_VOLDOWN:
#             setVOL(False)
#         elif event.value == KR_STUP:
#             setSTATION(True)
#         elif event.value == KR_STDOWN:
#             setSTATION(False)
#         # elif event.value== KR_D_UP:
#         #     print("dUP")
#         #     setVOL(False)
#         elif irval == 2099219:
#             print("DOWN")
#             setVOL(False)
#         elif irval == 2099222:
#             print("right")
#             setSTATION(True)
#         elif irval == 2099220:
#             print("left")
#             setSTATION(False)
#         elif irval == 2099278:
#             print("play")
#             os.system("mpc play")
#         elif irval == 2099277:
#             print("stop")
#             os.system("mpc stop")
#         elif irval == 2099204:
#             print("mute")
#             mute()
#         elif irval == 2099205:
#             print("tv")  # switch playlist
#             switchPLAYLIST()
#         elif irval == KR_OPT:
#             print("opt")  # start vol
#             startVol()
#         elif irval == 2099214:  # 10+
#             print("mail")
#             startTenPos()
#         elif irval == KR_POWER:  # 10+
#             print("reboot")
#             reboot()
#     sleep(0.01)
