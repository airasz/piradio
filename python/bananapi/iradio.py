#!/usr/bin/python
# -*- coding: utf-8 -*-
import keyboard
import os
import oledis
import iradio_oled
import textwrap
from time import sleep
import time
import random
import subprocess
from threading import *

# from sshkeyboard import listen_keyboard
display=iradio_oled.display()
VOLUME_UP = 115
VOLUME_DOWN = 114

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

myoled= oledis.oled()

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

def setVOL(up):
    status = ""
    if (getPlayState()) is True:
        # status = cmd("mpc volume " + "+5" if up else "-5")# if next else cmd("mpc prev")
        status = cmd("mpc volume +5") if up else cmd("mpc volume -5")
        # if up is True:
        #     status = cmd("mpc volume +5")
        # else:
        #     status = cmd("mpc volume -5")
    display.resettimer(status)
    displaytooled(status)

def setSTATION(next):
    status = ""
    ypos = random.randint(0,54)
    xpos = random.randint(0,50)
    if (getPlayState()) is True:
        display.display("playing next" if next else "playing previous", True)
        status = cmd("mpc next") if next else cmd("mpc prev")

    print("status = "+status)
    display.resettimer(status)
    displaytooled(status)


def playPos(pos):
    global TEN
    ypos = random.randint(0,54)
    xpos = random.randint(0,50)
    # display.display("playing pos "+ str(pos), (xpos,ypos))
    # display.display("playing pos "+ str(pos), True)
    display.display("playing pos "+ str(pos + 10 if TEN else pos), True)
    status = ""
    if TEN is True:
        global TOQ
        if TOQ > 10:
            pos = pos + 10
            status = cmd("mpc play " + str(pos))
            TEN = False
        else:
            status = cmd("mpc play " + str(pos))
    else:
        status = cmd("mpc play " + str(pos))
    display.resettimer(status)
    displaytooled(status)


def switchPLAYLIST():
    global SWITCH_PLAYLIST
    SWITCH_PLAYLIST = not SWITCH_PLAYLIST

    status = cmd("mpc clear")
    sleep(0.1)
    status = cmd("mpc load radio") if SWITCH_PLAYLIST else cmd("mpc load koplo")
    getstationlen()

    myoled.display(status, (0,0))
    sleep(1)
    status = cmd("mpc play")
    displaytooled(status)
    display.resettimer(status)


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

def millis():
  return round(time.time() * 1000)

PREVMILL=0;

def secondy():
    global PREVMILL
    if millis() > (PREVMILL + 1000):
        print("second")
        PREVMILL= millis()



while True:
    # try:
    ev = keyboard.read_event()
    print(ev.scan_code)
    # secondy()
    if ev.scan_code == VOLUME_UP and ev.event_type == keyboard.KEY_DOWN:
        setVOL(True)
    if ev.scan_code == VOLUME_DOWN and ev.event_type == keyboard.KEY_DOWN:
        setVOL(False)
    if ev.scan_code == NEXT and ev.event_type == keyboard.KEY_DOWN:
        setSTATION(True)
    if ev.scan_code == PREV and ev.event_type == keyboard.KEY_DOWN:
        setSTATION(False)
    if ev.scan_code == PLAY and ev.event_type == keyboard.KEY_DOWN:
        # os.system("mpc play")
        status = cmd("mpc play")
        displaytooled(status)
        getPlayState()
    if ev.scan_code == STOP and ev.event_type == keyboard.KEY_DOWN:
        # os.system("mpc play")
        status = cmd("mpc stop")
        # myoled.display("player stopped", (0,0))
        getPlayState()
    if ev.scan_code == MUTE and ev.event_type == keyboard.KEY_DOWN:
        mute()
    if ev.scan_code == SP and ev.event_type == keyboard.KEY_DOWN:
        switchPLAYLIST()
        getPlayState()
    if ev.scan_code == MUTE and ev.event_type == keyboard.KEY_DOWN:
        mute()
    for i in range(len(NUMKEYS)):
            if ev.scan_code == NUMKEYS[i][1]:
                playPos(NUMKEYS[i][0])
                break
    if ev.scan_code == 209 and ev.event_type == keyboard.KEY_DOWN:
        TEN = True
    # except:
    # print("device failed")
else:
    os.exit(0)
