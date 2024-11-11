#!usr/bin/env python
# import RPi.GPIO as GPIO
import time
import evdev
from evdev import InputDevice, categorize, ecodes
import os
from time import sleep
import serial

import asyncio
from evdev import InputDevice

SWITCH_PLAYLIST = False
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0
DBG_EVENT=False
EN_NEXMEDIA_R=False

#remot key nexmedia
KR_POWER = 2099200
KR_OPT = 2099287
KR_D_UP = 2099218
KR_D_DOWN = 2099219
KR_VOLUP = 2099202
KR_VOLDOWN = 2099203
KR_STUP = 2099206
KR_STDOWN = 2099207
KR_GREEN=2099225
KR_NUMKEYS=[[1 , 2099228],[2 , 2099229],[3 , 2099230],[4 , 2099264],[5 , 2099265],[6 , 2099266],[7 , 2099268],[8 , 2099269],[9 , 2099270],[10 , 2099271]]

KB_NUMKEYS=[[1 , 458841],[2 , 458842],[3 , 458843],[4 , 458844],[5 , 458845],[6 , 458846],[7 , 458847],[8 , 458848],[9 , 458849],[10 , 458850]]

#KB_NUMKEYS=[[1 , KEY_KP1],[2 , KEY_KP2],[3 , KEY_KP3],[4 , KEY_KP4],[5 , KEY_KP5],[6 , KEY_KP6],[7 , KEY_KP7],[8 , KEY_KP8],[9 , KEY_KP9],[10 , KEY_KP0]]


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

    con.write(status)
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
def processIR(irval):
    global EN_NEXMEDIA_R
    # print(irval)
    #hexval = hex(irval)
   # print(hexval)
    # sval=str(irval)
    if irval== KR_GREEN:
        EN_NEXMEDIA_R= not EN_NEXMEDIA_R
    if EN_NEXMEDIA_R:
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
        
def processKB(kval):
    print("processKB"+ str(kval))
    for i in range(len(KB_NUMKEYS)):
        # NKV=int(KR_NUMKEYS[i][1])
        # NKI=int (KR_NUMKEYS[i][0])
        if kval == KB_NUMKEYS[i][1]:
            playPos(KB_NUMKEYS[i][0])
            break

VOLUME_UP = 115
VOLUME_DOWN = 114

NEXT = 163
PREV = 165
PLAY = 164
STOP = 166
#SWITCH_PLAYLIST = True
#MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0
T_LINES = 0
#TEN = False
#TOQ=0

NUMKEYS=[[1 , 79],[2 , 80],[3 , 81],[4 ,75],[5 , 76],[6 , 77],[7 ,71],[8 , 72],[9 , 73],[10 , 82]]


def processKboard(ecode):
    if ecode == VOLUME_UP:
        setVOL(True)
    if ecode == VOLUME_DOWN:
        setVOL(False)
    if ecode == NEXT:
        setSTATION(True)
    if ecode == PREV:
        setSTATION(False)
    if ecode == PLAY:
        os.system("mpc play")
        # status = cmd("mpc play")
        getPlayState()
    if ecode == STOP:
        os.system("mpc stop")
        # status = cmd("mpc stop")
        # myoled.display("player stopped", (0,0))
        getPlayState()
    if ecode == MUTE:
        mute()
    if ecode == SP:
        switchPLAYLIST()
        getPlayState()
    if ecode == MUTE:
        mute()
    for i in range(len(NUMKEYS)):
            if ecode == NUMKEYS[i][1]:
                playPos(NUMKEYS[i][0])
                break
    if ecode == 209:
        TEN = True

saved_eval=0
async def OLD_print_events(device):
    async for event in device.async_read_loop():
        #print(device.path, evdev.categorize(event), sep=': ')
        #print(device.path, event.value, sep=': ')
        global saved_eval
        if event.value>10:
            saved_eval=event.value
            if DBG_EVENT is True:
                print("saved_eval= " + str(saved_eval))

        if DBG_EVENT is True:
            print("ev_key= "+str(ecodes.EV_KEY))
            print("etype= "+str(event.type))
            print("ecode= " + str(event.code))
            print("evalue= " + str(event.value))
        if event.type == ecodes.EV_KEY:
            c=categorize(event)
            print("keystate= " + str(c.keystate))
            if c.keystate==c.key_down:
                if DBG_EVENT is True:
                    print(c.keycode)
            if event.value==0:
                if DBG_EVENT is True:
                    print("keyboard typed")
                    print("KBev_key= "+str(ecodes.EV_KEY))
                    print("KBetype= "+str(event.type))
                    print("KBecode= " + str(event.code))
                processKB(saved_eval)
        else:
            print("processIR")
            processIR(event.value)
        
        #print(event.code)
        

async def print_events(device):
    async for event in device.async_read_loop():
        #print(device.path, evdev.categorize(event), sep=': ')
        #print(device.path, event.value, sep=': ')
        global saved_eval


        if event.value>200000:
            saved_eval=event.value
            if DBG_EVENT is True:
                print("saved_eval= " + str(saved_eval))


        if DBG_EVENT is True:
            print("ev_key= "+str(ecodes.EV_KEY))
            print("etype= "+str(event.type))
            print("ecode= " + str(event.code))
            print("evalue= " + str(event.value))
        if event.type == ecodes.EV_KEY:
            c=categorize(event)
            print("keystate= " + str(c.keystate))
            if c.keystate==c.key_up:#0=up, 1=hold, 2=down
                # processKB(saved_eval)
                processKboard(event.code)
                # print(c.keycode)
                # print("c key code= "+str(c.keycode))
                # print(c.keycode)
            # if event.value==0:
            #     print("keyboard typed")
            #     print("KBev_key= "+str(ecodes.EV_KEY))
            #     print("KBetype= "+str(event.type))
            #     print("KBecode= " + str(event.code))
            #     processKB(saved_eval)
        else:
            if DBG_EVENT is True:
                print("processIR")
            processIR(event.value)
        if DBG_EVENT is True:
            print("===============end debug==========")
        #print(event.code)
#for device in ir, keybd:
    #asyncio.ensure_future(print_events(device))

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.name)
    if device.name == "sunxi-ir":
        print("Using device", device.path, "\n")
        #return device
    # print("No device found!")
    asyncio.ensure_future(print_events(device))


# Serial setup connection
con = serial.Serial(

    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)


loop = asyncio.get_event_loop()
loop.run_forever()




#
# try:
#     event_list = [event.value for event in events]
#     print("Receved command:", event_list)
# except BlockingIOError:
#     print("No commands received. \n")


# dev = InputDevice('/dev/input/event1')


