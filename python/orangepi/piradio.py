#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import keyboard
import os
import oledis
import iradio_oled
import textwrap
from time import sleep
import time
import random
import serial
import subprocess
from threading import *
import json

import mpcstimer

# from sshkeyboard import listen_keyboard
display=iradio_oled.display()
myoled= oledis.oled()
stimer=mpcstimer.mpctimer()

VOLUME_UP = 115
VOLUME_DOWN = 114

EN_NEXMEDIA_R=False
NEXT = 163
PREV = 165
PLAY = 164
STOP = 166
SWITCH_PLAYLIST = True
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0
T_LINES = 0
TEN = False
TOQ=0

NUMKEYS=[[1 , 79],[2 , 80],[3 , 81],[4 ,75],[5 , 76],[6 , 77],[7 ,71],[8 , 72],[9 , 73],[10 , 82]]

KR_nNUM=[[1, "41038C7"],[2, "410B847"],[3, "4107887"],[4, "41002FD"],[5, "410827D"],[6, "41042BD"],[7, "41022DD"],[8, "410A25D"],[9, "410629D"],[0, "410E21D"]]

KR_cNUM=[[1, "FF30CF"],[2, "FFB04F"],[3, "FF708F"],[4, "FF08F7"],[5, "FF8877"],[6, "FF48B7"],[7, "FF28D7"],[8, "FF04FB"],[9, "FF847B"],[0, "FF44BB"]]
#temporary flag
TEN = False
NUM_VOL=0
MIN_SLEEP=0
MIN_SLEEPV=0
TO_REBOOT= False
TS_ENABLE=False
STOP_SLEEP=0
# PLAYlists

KR_RIGHT    	="4106897"
KR_LEFT     	="41028D7"
KR_UP       	="41048B7"
KR_DOWN     	="410C837"
KR_VOLUP 	    ="41040BF"
KR_VOLDOWN 	    ="410C03F"
KR_STUP 	    ="410609F"
KR_STDOWN 	    ="410E01F"
KR_PLAY     	="410728D"
KR_STOP     	="410B24D"
KR_PAUSE    	="410C23D"
KR_POWER    	="41000FF"
KR_MUTE     	="41020DF"
KR_ENTER    	="410A857"
KR_102ND    	="410708F"
KR_9        	="410629D"
KR_TV       	="410A05F"
KR_OPT       	="410EA15" #preset volume"
KR_MAIL         ="410708F" #preset station
KR_YELLOW       ="41058A7"
KR_SLEEP        ="410F807"
KR_OK           ="410A857"
KR_EXIT         ="41008F7"

KRC_VOLUP 	    ="FFF20D"
KRC_VOLDOWN 	="FFAA55"
KRC_STUP 	    ="FF9A65"
KRC_STDOWN 	    ="FF6A95"
KRC_PLAY     	="FF24DB"
KRC_POWER    	="FFC43B"
KRC_MUTE     	="FF827D" #stop
KRC_MENU    	="FFCA35"
KRC_MODE       	="FF2AD5" #swich playlist
KRC_CALL       	="FF8A75" #preset volume"
KRC_CCALL       ="FFFA05" #preset station 10+

CDOWN=0

# os.system("/usr/bin/python mpcsleeper.py && exit 0")
# try:
#     os.system("/usr/bin/python mpcsleeper.py | exit 0")
# except:
    # print("cannot start mpc sleep timer")

def interuptDisplay(delay, fontsize, msg):
    if fontsize==0:
        display.frezeeDisplay(delay)
        display.display(msg, False)

def load_variable():
    global CDOWN
    global TS_ENABLE
    try:
        with open("/home/timer.json", "r") as f:
            data = json.load(f)
            CDOWN = data.get("seconds", CDOWN)
            TS_ENABLE= data.get("enable", False)
    except FileNotFoundError:
        pass


def cmd(cmd):
    rtr=""
    try:
        rtr= subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        rtr=e.output
        # rtr="eror"

    rtr= rtr.decode("utf-8")
    return rtr

def getVol():
    status = "radio volume: 50%"
    # os.system("mpc status")
    # os.system("mpc status > tmp")
    # status =  open('tmp', 'r').read()

    # status = os.popen("mpc").read()
    status = subprocess.check_output("mpc", shell=True)
    status =  status.decode("utf-8")
    # myoled.display(status, (0,0))
    displaytooled(status)
    # print("s="+status )
    volpos = status.index('volume')
    print(volpos)
    volstatus = status[volpos:volpos+13]

    print("volstatus        ="+volstatus )
    percenpos = volstatus.index('%')
    svol = volstatus[8:percenpos]

    print("svol="+svol )
    vol = int(svol)

    print("vol="+   str(vol) )
    global P_VOL
    P_VOL = vol

def mute():
    getVol()
    print("P_VOL="+str(P_VOL) )
    if P_VOL > 0:
        global C_VOL
        C_VOL =P_VOL
        # os.system("mpc volume 0")
        status = cmd("mpc volume 0")
    else:
        status = cmd("mpc volume " + str(C_VOL))

def getPlayState():
    status = ""
    status = cmd("mpc")

    if 'playing' in status:
        return True
    else:
        return False


def startVol():
    display.frezeeDisplay(8)
    display.displayfs("jump volume...", 15)
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    if TEN is True:
        TEN =False
    NUM_VOL=1
    MIN_SLEEP=0


stimerStop=0
def startsetsleep():
    global stimerStop
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    global TS_ENABLE
    load_variable()
    if TS_ENABLE is True:
        if stimerStop==0:
            display.frezeeDisplay(3)
            display.display("timer is running\npress again to stop", False)
            stimerStop+=1
        elif stimerStop==1:
            jdata={"enable":False,
                "startrun":False,
                "svalue":0,
                "seconds":0
            }
            display.frezeeDisplay(3)
            with open("/home/timer.json", "w") as f:
                json.dump(jdata, f)
            display.display("timer is stopped", False)
            stimerStop=0
    else:
        display.frezeeDisplay(8)
        display.display("set sleep...", True)
        MIN_SLEEP=1

def startTenPos():
    display.frezeeDisplay(8)
    display.display("jump station to...", True)
    global TEN
    global NUM_VOL
    global MIN_SLEEP
    TEN = True
    if NUM_VOL !=0:
        NUM_VOL=0
    MIN_SLEEP=0

def setSTATION(next):
    status = ""
    ypos = random.randint(0,54)
    xpos = random.randint(0,50)
    if (getPlayState()) is True:
        # display.display("playing next" if next else "playing previous", True)
        display.displayfs("playing\nnext" if next else "playing\nprevious", 18)
        status = cmd("mpc next") if next else cmd("mpc prev")

    print("status = "+status)
    display.frezeeDisplay(3)
    # displaytooled(status)


def setVOL(up):
    status = ""
    if (getPlayState()) is True:
        status = subprocess.check_output("mpc volume | awk '{print$2}'", shell=True)
        vol=str(status.decode("utf-8"))
        vol=vol[:len(vol)-2]
        intvol = int(vol)
        # status = cmd("mpc volume " + "+5" if up else "-5")# if next else cmd("mpc prev")
        status = cmd("mpc volume +5") if up else cmd("mpc volume -5")

        # if up is True:
        #     status = cmd("mpc volume +5")
        # else:
        #     status = cmd("mpc volume -5")
    print("vol"+vol)
    # display.displaybig("v"+vol)
    display.frezeeDisplay(3)
    display.displayfs("v"+vol, 25)


def reboot():
    global TO_REBOOT
    if TO_REBOOT is False:
        TO_REBOOT = True
        # display.display("goto reboot", True)
        display.frezeeDisplay(5)
        myoled.displayfs("press again\nto reboot", 16)
    else:
        display.frezeeDisplay(5)
        myoled.displayfs("rebooting...", 16)
        sleep(1)
        os.system("reboot")


def exitset():
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    global STOP_SLEEP
    global MIN_SLEEPV
    global TO_REBOOT
    TEN = False
    NUM_VOL = 0
    STOP_SLEEP = False
    MIN_SLEEP = 0
    myoled.displayfs("operation\ncanceled", 16)
    display.frezeeDisplay(2)
    # display.onmenu(False)


VOLTO=0
def clickNum(pos):
    global TEN
    global VOLTO
    global NUM_VOL
    global MIN_SLEEP
    global MIN_SLEEPV
    ypos = random.randint(0,54)
    xpos = random.randint(0,50)
    # display.display("playing pos "+ str(pos), (xpos,ypos))
    # display.display("playing pos "+ str(pos), True)

    status = ""
    if TEN is True:
        display.display("playing pos "+ str(pos + 10 if TEN else pos), True)
        global TOQ
        if TOQ > 10:
            pos = pos + 10
            # display.display("play pos "+ str(pos), True)
            myoled.displayfs("play pos "+ str(pos),15)
            display.frezeeDisplay(3)
            os.system("mpc play " + str(pos))
            TEN = False
        else:
            # display.display("play pos "+ str(pos), True)
            myoled.displayfs("play pos "+ str(pos),15)
            display.frezeeDisplay(3)
            os.system("mpc play " + str(pos))

    else:
        # display.display("volume to "+ str(pos + 10 if TEN else pos), True)
        if NUM_VOL==0 and MIN_SLEEP==0:
            # display.display("play pos "+ str(pos), True)
            myoled.displayfs("play pos "+ str(pos),15)
            display.frezeeDisplay(3)
            os.system("mpc play " + str(pos))
            return
        if NUM_VOL == 1:
            VOLTO=pos * 10
            # display.display("volume to "+ str(pos)+"x", True)
            myoled.displayfs("volume to\n"+ str(pos)+"x",15)
            display.frezeeDisplay(3)
            print("start vol========== "+ str(VOLTO))
            NUM_VOL =2
        elif NUM_VOL == 2:
            VOLTO+= pos
            NUM_VOL=0
            # display.display("volume to "+ str(VOLTO), True)
            myoled.displayfs("set volume to\n"+ str(VOLTO),15)
            display.frezeeDisplay(3)
            os.system("mpc volume " + str(VOLTO))

        if MIN_SLEEP==1:
            # MIN_SLEEPV+=pos**MIN_SLEEP
            MIN_SLEEPV=0
            MIN_SLEEPV=pos*10
            # display.display("sleep in "+ str(pos)+"x minutes", False)
            myoled.displayfs("sleep in\n"+ str(pos)+"x minutes",15)
            display.frezeeDisplay(8)
            MIN_SLEEP=2
        elif MIN_SLEEP==2:
            MIN_SLEEPV+=pos
            # display.display("sleep in "+ str(MIN_SLEEPV)+" minutes\nClick OK to confirm", False)
            myoled.displayfs("sleep in\n"+ str(MIN_SLEEPV)+" minutes\nClick OK to\nconfirm",15)
            display.frezeeDisplay(8)





    # display.frezeeDisplay(3)
    # displaytooled(status)


def switchPLAYLIST():
    global SWITCH_PLAYLIST
    # global PLAYlists
    # SWITCH_PLAYLIST = not SWITCH_PLAYLIST
    getstationlen()
    if SWITCH_PLAYLIST is True:
        SWITCH_PLAYLIST =False
    else:
        SWITCH_PLAYLIST=True

    print("SWITCH_PLAYLIST="+str(SWITCH_PLAYLIST))
    # import os

    # status = os.popen("ls /var/lib/mpd/playlists/").read()
    status = cmd("ls /var/lib/mpd/playlists/")
    status = status.replace(".m3u", "")
    PLAYlists = status.split()
    # print(PLAYlists[0])
    # length = len(starr)
    # for i in PLAYlists:
    #     print(str(PLAYlists[i]))


    # length = len(PLAYlists)
    # for i in range(length):
    #     print(PLAYlists[i])

    status = cmd("mpc clear")
    sleep(0.1)
    print(("mpc load " + PLAYlists[0]) if SWITCH_PLAYLIST else ("mpc load " + PLAYlists[1]))
    status = cmd("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else cmd("mpc load " + PLAYlists[0])
    getstationlen()
    status= status.replace(" ", "\n")
    myoled.displayfs(status, 16)
    display.frezeeDisplay(2)
    sleep(1)
    status = cmd("mpc play")
    displaytooled(status)
    display.frezeeDisplay(3)


def getstationlen(): #get total playlist
    global T_LINES
    global TOQ
    global SWITCH_PLAYLIST
    status = subprocess.check_output("mpc playlist", shell=True)
    status =  status.decode("utf-8")
    if "radioislam" in status:
        SWITCH_PLAYLIST = True
    T_LINES = status.count('\n')
    TOQ = T_LINES
    print("playlist="+ str(T_LINES))
    # print(T_LINES)


def displaytooled(status):
    if "volume" not in status:
        return
    mlpl = 22# maximum length per line
    if "[" not in status:
        return

    sm=""
    text=""
    #srink status
    inrep = status.index("repeat")
    status= status[:inrep]

    # crop station info
    inbrace =status.index("[")
    station = status[:inbrace]
    if len(station)>44:
        station = station[0:44]
    # print("station = " + station)
    # split limited length char to list
    infolist=textwrap.wrap(station, mlpl)

    # crop playing info
    indvol=status.index("volume")
    indel=status.index("/")+3
    state=status[inbrace:indel]
    state=state.replace("/", " - ")
    state=state.replace("#", " ")
    # split limited length char to list
    msglist=textwrap.wrap(state, mlpl)

    #crop volume info
    stvol=status[indvol:]

    # print("state = " + state)

    msglist.append(stvol)
    for i in infolist:
        msglist.append(i)

    status= status.replace("(0%)", "")
    status= status.replace("(volume", "\nvolume")

    # myoled.display(status, (0,0))
    totline=len(msglist)
    # print(totline)
    sm=""
    text=""
    totpage=int(len(msglist)/4)
    ttlline=4*totpage
    if totline> ttlline:
        totpage+=1 #get actual page

    # print("total dirt line = " + str(ttlline))
    # print(totpage)

#    print("P_COUNT = " + str(P_COUNT))
    for x in range(totline):
        sm=str(msglist[x])
        text += sm
        text +="\n"


        # print(text)
    myoled.display(text, (0,0))
    print("to display="+text)

getPlayState()
getstationlen()

def msleep(minutes):
    stimer.startcdown(minutes)

def ok():
    global MIN_SLEEP
    global MIN_SLEEPV
    if MIN_SLEEP>0:
        # stimer.startcdown(MIN_SLEEPV)
        os.system("/usr/bin/python startsleeper.py "+ str(MIN_SLEEPV))
        # display.display("starting sleep timer\n", True)
        myoled.displayfs("starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes",15)
        display.frezeeDisplay(3)
        MIN_SLEEP=0

def millis():
  return round(time.time() * 1000)

PREVMILL=0;

def secondy():
    global PREVMILL
    if millis() > (PREVMILL + 1000):
        print("second")
        PREVMILL= millis()

ser = serial.Serial(
        port='/dev/ttyS5', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
)
def processIR(irval):
    global EN_NEXMEDIA_R
    if irval== KR_YELLOW:
        EN_NEXMEDIA_R= not EN_NEXMEDIA_R
        display.display("REMOTE control\n"+("unlocked" if EN_NEXMEDIA_R else "locked"), False)
        display.frezeeDisplay(3)
        return
    if EN_NEXMEDIA_R:
        for i in range(len(KR_nNUM)):
            if irval == KR_nNUM[i][1]:
                clickNum(KR_nNUM[i][0])
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
        elif irval == KR_DOWN:
            print("DOWN")
            setVOL(False)
        elif irval == KR_RIGHT:
            print("right")
            setSTATION(True)
        elif irval == KR_LEFT:
            print("left")
            setSTATION(False)
        elif irval == KR_PLAY:
            print("play")
            os.system("mpc play")
        elif irval == KR_STOP:
            print("stop")
            os.system("mpc stop")
        elif irval == 2099204:
            print("mute")
            mute()
        elif irval == KR_TV:
            print("tv")  # switch playlist
            switchPLAYLIST()
        elif irval == KR_OPT:
            print("opt")  # start vol
            startVol()
        elif irval == KR_MAIL:  # 10+
            print("mail")
            startTenPos()
        elif irval == KR_POWER:  # 10+
            print("reboot")
            reboot()
        elif irval==KR_SLEEP:
            # msleep(20)
            startsetsleep()
        elif irval==KR_OK:
            ok()
        elif irval==KR_EXIT:
            exitset()
    else:
        if irval[:2]=="41":
            # interuptDisplay(3,  unregistered key remote\nor this remote locked")
            display.display("unregistered key remote\nor this remote locked", False)
            display.frezeeDisplay(3)


def processIRc(irval):
    for i in range(len(KR_cNUM)):
        if irval == KR_cNUM[i][1]:
            clickNum(KR_cNUM[i][0])
            break
    if irval == KRC_VOLUP:
        print("volume up")
        setVOL(True)
    elif irval == KRC_VOLDOWN:
        setVOL(False)
    elif irval == KRC_STUP:
        setSTATION(True)
    elif irval == KRC_STDOWN:
        setSTATION(False)
    elif irval == KRC_PLAY:
        global MIN_SLEEP
        if MIN_SLEEP>0:
            ok()
        else:
            print("play")
            os.system("mpc play")
    elif irval == KRC_MUTE:
        print("mute > stop")
        os.system("mpc stop")
    elif irval == KRC_MODE:
        print("mode > switch playlist")  # switch playlist
        switchPLAYLIST()
    elif irval == KRC_CALL:
        print("call > vol jump")  # start vol
        startVol()
    elif irval == KRC_CCALL:  # 10+
        print("ccall > ten+")
        startTenPos()
    elif irval == KRC_POWER:  # 10+
        print("reboot")
        reboot()
    elif irval == KRC_POWER:  # 10+
        print("get net data")
    elif irval == KRC_MENU:
        startsetsleep()



while True:
    x=ser.readline()
    s=x.decode("utf-8")
    ss=s[:2]
    if ss == "FF":
        processIRc(s)
    elif ss == "41":
        processIR(s)
        # print (s)
    # print ("ss="+ss)
    sleep(0.01)
    # except:
    # print("device failed")
else:
    os.exit(0)
