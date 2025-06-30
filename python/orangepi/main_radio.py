#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import keyboard
import os
import sys
import textwrap
from time import sleep
import time
import random
import serial
import subprocess
from threading import *
import threading
import json
import asyncio
import serial_asyncio
import socket
import signal

import oledis
import module_radio
# import mpcstimer

import tornado
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
# import wsradio

# from sshkeyboard import listen_keyboard
display=module_radio.display()
mtimer=module_radio.tasktimer()

# myoled= oledis.oled()
sleeptimer= module_radio.sleeptimer()
# stimer=mpcstimer.mpctimer()
# ws=wsradio.WSHandler()
# ws=wsradio
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
PLAY_CURL=False
PLAYLIST_X=0;
splp=False
GOTOSTATION=False

NUMKEYS=[[1 , 79],[2 , 80],[3 , 81],[4 ,75],[5 , 76],[6 , 77],[7 ,71],[8 , 72],[9 , 73],[10 , 82]]

KR_nNUM=[[1, "41038C7"],[2, "410B847"],[3, "4107887"],[4, "41002FD"],[5, "410827D"],[6, "41042BD"],[7, "41022DD"],[8, "410A25D"],[9, "410629D"],[10, "410E21D"]]

KR_cNUM=[[1, "FF30CF"],[2, "FFB04F"],[3, "FF708F"],[4, "FF08F7"],[5, "FF8877"],[6, "FF48B7"],[7, "FF28D7"],[8, "FF04FB"],[9, "FF847B"],[10, "FF44BB"]]

KR_wNUM= [[1,"FD40BF"],[2,"FDC03F"],[3,"FD20DF"],[4,"FDA05F"],[5,"FD609F"],[6,"FDE01F"],[7,"FD10EF"],[8,"FD906F"],[9,"FD50AF"],[10,"FD30CF"]]

KR_eNUM=[[1 , "FD4AB5"],[2 , "FD0AF5"],[3 , "FD08F7"],[4 , "FD6A95"],[5 , "FD2AD5"],[6 , "FD28D7"],[7 , "FD728D"],[8 , "FD32CD"],[9 , "FD30CF"],[10 , "FDF00F"]]
#temporary flag
TEN = False
NUM_VOL=0
MIN_SLEEP=0
MIN_SLEEPV=0
TO_REBOOT= False
TS_ENABLE=False
STOP_SLEEP=0
RADIOSLEEPTIMERENABLED=True
RADIOSECONDSLEEPTIMER=3600
USERSLEEPTIMERENABLED=True
USERSECONDSLEEPTIMER=3600
PLAYlists=[]


#EVERCROSS

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

# REMOTE PUTIH"
KW_POWER= "FD00FF"
KW_MUTE= "FD807F"
KW_SLEEP= "FDC23D"
KW_VOLUP= "FD12ED"
KW_VOLDOWN= "FD926D"
KW_STUP= "FD52AD"
KW_STDOWN= "FDD22D"
KW_PLAY= "FD8A75"
KW_STOP= "FD4AB5"
KW_ENTER= "FD08F7"
KW_TEN= "FDD02F" #-/--
KW_SVOL= "FDB04F"
KW_INPUT = "FDF00F"

#EVERCROSS
KRE_POWER  ="FD9A65"
KRE_MUTE  ="FD9867"
KRE_VOLUP  ="FDD827"
KRE_VOLDOWN     ="FD5AA5"
KRE_STUP  ="FD609F"
KRE_STDOWN  ="FD6897"
KRE_TV   ="FDA857"
KRE_RECALL  ="FDC837"
KRE_INFO  ="FDE817"
KRE_PLAY  ="FD629D"
KRE_PAUSE  ="FD22DD"
KRE_STOP  ="FD20DF"
KRE_RED      ="FD42BD"
KRE_GREEN  ="FD02FD"
KRE_LIME  ="FD00FF"
KRE_TIMER  ="FDC03F"
KRE_OK   ="FD58A7"
KRE_FAV="FDAA55"
KRE_EXIT="FDA05F"
KRE_PAGEUP       ="FDB04F"
KRE_PAGEDOWN="FD8877"
KRE_GOTO="FD708F"

CDOWN=0


file_path = "radioconfig.json"

# os.system("/usr/bin/python mpcsleeper.py && exit 0")
# try:
#     os.system("/usr/bin/python mpcsleeper.py | exit 0")
# except:
    # print("cannot start mpc sleep timer")

def interuptDisplay(delay, fontsize, msg):
    if fontsize==0:
        display.frezeeDisplay(delay)
        display.display(msg, False)
    else:
        display.frezeeDisplay(delay)
        display.displayfs(msg, fontsize)
        # display.display(msg, False)


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

def load_config():
    global REMOTES
    global CONFIGDATA
    global RNEXMEDIA
    global RPUTIH
    global RCAR
    global REVERCROSS
    try:
        with open(file_path, "r") as f:
            CONFIGDATA = json.load(f)
            REMOTES=CONFIGDATA.get("remote","")
            if CONFIGDATA.get("autoload","true") is True:
                os.system("mpc play")
                print("auto play by config")
            # else:
            #     os.system("mpc stop")
            #     print("auto stop by config")
            # print("remote array: "+ str(REMOTES))
            # for item in CONFIGDATA.get("remote",""):
            #     print("item: "+ str(item))
            #     print("name:"+ str(item.get("name","noname")))
            #
            # for itm in REMOTES:
            #     print("remotename:"+ str(itm["name"]))
    except FileNotFoundError:
        pass

load_config()
def cmd(cmd):
    rtr=""
    try:
        rtr= subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        rtr=e.output
        # rtr="eror"

    rtr= rtr.decode("utf-8")
    return rtr

def loadPLAYlists():
    global PLAYlists
    # status = cmd("ls /var/lib/mpd/playlists/")
    # status = status.replace(".m3u", "")
    # PLAYlists = status.split()
    sr=subprocess.check_output("mpc lsplaylists", shell=True).decode("utf-8")
    PLAYlists=sr.splitlines(keepends=False)
loadPLAYlists()

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
    # display.frezeeDisplay(8)
    # display.displayfs("jump volume...", 15)
    interuptDisplay(8, 15, "jump volume...")
    exitset(False)
    global NUM_VOL
    NUM_VOL=1



stimerStop=0
def startsetsleep():
    exitset(False)
    global stimerStop
    global MIN_SLEEP
    global TS_ENABLE

    # load_variable()
    if sleeptimer.isrunning() is True:
        if stimerStop==0:
            # display.frezeeDisplay(3)
            # display.display("timer is running\npress again to stop", False)
            interuptDisplay(3, 0, "timer is running\npress again to stop")
            stimerStop+=1
        elif stimerStop==1:
            # jdata={"enable":False,
            #     "startrun":False,
            #     "svalue":0,
            #     "seconds":0
            # }
            display.frezeeDisplay(3)
            # with open("/home/timer.json", "w") as f:
            #     json.dump(jdata, f)
            sleeptimer.stopcdown()
            # display.display("timer is stopped", False)
            interuptDisplay(3, 0, "timer is stopped")
            stimerStop=0
    else:
        # display.frezeeDisplay(8)
        # display.display("set sleep...", True)
        interuptDisplay(8, 0, "set sleep...")
        MIN_SLEEP=1

def startTenPos():
    # display.frezeeDisplay(8)
    # display.display("jump station to...", True)
    interuptDisplay(8, 0, "jump station to\n10 + ...")
    exitset(False)
    global TEN
    TEN = True

def startPlistTo():
    exitset(False)
    global splp
    splp=True
    pls=""
    ids=0
    for item in PLAYlists:
        pls+=(f'{str(ids+1)}. {str(item)}\n')
        ids+=1
    # display.frezeeDisplay(8)
    # display.display(f'select.\n{pls}', False)
    interuptDisplay(8, 0, f'select.\n{pls}')

def setSTATION(next):
    status = ""
    ypos = random.randint(0,54)
    xpos = random.randint(0,50)
    display.frezeeDisplay(3)
    if (getPlayState()) is True:
        # display.display("playing next" if next else "playing previous", True)
        # display.frezeeDisplay(2)
        # display.displayfs("playing\nnext" if next else "playing\nprevious", 18)
        interuptDisplay(2, 18, "playing\nnext" if next else "playing\nprevious")
        status = cmd("mpc next") if next else cmd("mpc prev")

    print("status = "+status)
    broadcast_message("resettimer")
    # displaytooled(status)

def getCurrentStation():

    status = "radio volume: 50%"
    status = subprocess.check_output("mpc", shell=True)
    status =  status.decode("utf-8")
    ps = status.index(']')
    pps=status.index('%')
    pss=status[ps:pps]
    ht=pss.index("#")
    fs=pss.index('/')
    cs=pss[ht+1:fs]
    return int(cs)

def stationPage(next):
    global TOQ
    status = ""
    cs= getCurrentStation()
    if next :
        cs= cs+10
        if cs> TOQ:
            cs=TOQ
        interuptDisplay(3, 15, "play pos "+ str(cs))
        status = subprocess.check_output(f"mpc play {cs}", shell=True)
        status =  status.decode("utf-8")
    else:
        cs= cs-10
        if cs< 1:
            cs=1
        interuptDisplay(3, 15, "play pos "+ str(cs))
        status = subprocess.check_output(f"mpc play {cs}", shell=True)
        status =  status.decode("utf-8")


def setVOL(up):
    status = ""
    vol=""
    status = subprocess.check_output(("mpc volume +5 | grep volume | awk '{print$2}'") if up else ("mpc volume -5 | grep volume | awk '{print$2}'"), shell=True).decode("utf-8")
    print("vol "+status)
    # display.displaybig("v"+vol)
    # display.frezeeDisplay(3)
    # display.displayfs("v "+status, 25)
    interuptDisplay(3, 25, "v "+status)
    broadcast_message("vol="+status)


def reboot():
    global TO_REBOOT
    if TO_REBOOT is False:
        TO_REBOOT = True
        # display.display("goto reboot", True)
        # display.frezeeDisplay(8)
        # myoled.displayfs("press again\nto reboot", 16)
        interuptDisplay(8, 16, "press again\nto reboot")
    else:
        # display.frezeeDisplay(3)
        # myoled.displayfs("rebooting...", 16)
        interuptDisplay(3, 16, "rebooting...")
        sleep(1)
        os.system("reboot")


def exitset(info):
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    global STOP_SLEEP
    global MIN_SLEEPV
    global TO_REBOOT
    global splp
    global GOTOSTATION
    GOTOSTATION=False
    splp=False
    TEN = False
    NUM_VOL = 0
    STOP_SLEEP = False
    MIN_SLEEP = 0
    if info:
        # display.frezeeDisplay(2)
        # myoled.displayfs("operation\ncanceled", 16)
        interuptDisplay(3, 16, "operation\ncanceled")
    # display.onmenu(False)


VOLTO=0
def clickNum(pos):
    global TEN
    global VOLTO
    global NUM_VOL
    global MIN_SLEEP
    global MIN_SLEEPV
    global splp
    ypos = random.randint(0,54)
    xpos = random.randint(0,50)
    # display.display("playing pos "+ str(pos), (xpos,ypos))
    # display.display("playing pos "+ str(pos), True)

    status = ""
    if TEN is True:
        display.display("playing pos "+ str(pos + 10 if TEN else pos), True)
        global TOQ # total queue
        if TOQ > 10:
            pos = pos + 10
            # display.display("play pos "+ str(pos), True)
            # display.frezeeDisplay(3)
            # myoled.displayfs("play pos "+ str(pos),15)
            interuptDisplay(3, 15, "play pos "+ str(pos))
            os.system("mpc play " + str(pos))
            TEN = False
        else:
            # display.display("play pos "+ str(pos), True)
            # display.frezeeDisplay(3)
            # myoled.displayfs("play pos "+ str(pos),15)
            interuptDisplay(3, 15, "play pos "+ str(pos))
            os.system("mpc play " + str(pos))
        broadcast_message("resettimer")

    else:
        # display.display("volume to "+ str(pos + 10 if TEN else pos), True)
        if NUM_VOL==0 and MIN_SLEEP==0 and splp is False:
            # display.display("play pos "+ str(pos), True)
            # display.frezeeDisplay(3)
            # myoled.displayfs("play pos "+ str(pos),15)
            interuptDisplay(3, 15, "play pos "+ str(pos))
            os.system("mpc play " + str(pos))
            broadcast_message("resettimer")
            return
        if NUM_VOL == 1:
            VOLTO=pos * 10
            # display.display("volume to "+ str(pos)+"x", True)
            # display.frezeeDisplay(5)
            # myoled.displayfs("volume to\n"+ str(pos)+"x",15)
            interuptDisplay(5, 15, "volume to\n"+ str(pos)+"x")
            print("start vol========== "+ str(VOLTO))
            NUM_VOL =2
            broadcast_message("resettimer")
        elif NUM_VOL == 2:
            VOLTO+= pos
            NUM_VOL=0
            # display.display("volume to "+ str(VOLTO), True)
            # display.frezeeDisplay(5)
            # myoled.displayfs("set volume to\n"+ str(VOLTO),15)
            interuptDisplay(5, 15, "set volume to\n"+ str(VOLTO))
            os.system("mpc volume " + str(VOLTO))
            broadcast_message("resettimer")

        if MIN_SLEEP==1:
            # MIN_SLEEPV+=pos**MIN_SLEEP
            MIN_SLEEPV=0
            MIN_SLEEPV=pos*10
            # display.display("sleep in "+ str(pos)+"x minutes", False)
            # display.frezeeDisplay(5)
            # myoled.displayfs("sleep in\n"+ str(pos)+"x minutes",15)
            interuptDisplay(5, 15, "sleep in\n"+ str(pos)+"x minutes")
            MIN_SLEEP=2
        elif MIN_SLEEP==2:
            MIN_SLEEPV+=pos
            # display.display("sleep in "+ str(MIN_SLEEPV)+" minutes\nClick OK to confirm", False)
            # display.frezeeDisplay(8)
            # myoled.displayfs("sleep in\n"+ str(MIN_SLEEPV)+" minutes\nClick OK to\nconfirm",13)
            interuptDisplay(8, 13,"sleep in\n"+ str(MIN_SLEEPV)+" minutes\nClick OK to\nconfirm")
        if splp is True:
            # status = cmd("ls /var/lib/mpd/playlists/")
            # status = status.replace(".m3u", "")
            # PLAYlists = status.split()


            status = cmd("mpc clear")
            sleep(0.1)
            # print(("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else ("mpc load " + PLAYlists[0]))
            # status = cmd("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else cmd("mpc load " + PLAYlists[0])
            if pos < len(PLAYlists)+1:
                status= cmd("mpc load " + PLAYlists[pos-1])
                getstationlen()
                status= status.replace(" ", "\n")
                # display.frezeeDisplay(2)
                # myoled.displayfs(status, 16)
                interuptDisplay(2, 16,status)
                sleep(1)
                status = cmd("mpc play")
                # displaytooled(status)
                broadcast_message("info="+status)
                display.frezeeDisplay(3)
            splp=False


    # display.frezeeDisplay(3)
    # displaytooled(status)


def switchPLAYLIST():
    global SWITCH_PLAYLIST
    global PLAY_CURL
    global PLAYLIST_X
    global PLAYlists
    PLAY_CURL=False
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

    PLAYLIST_X+=1
    if PLAYLIST_X == len(PLAYlists):
        PLAYLIST_X=0
    # print(PLAYlists[0])
    # length = len(starr)
    # for i in PLAYlists:
    #     print(str(PLAYlists[i]))


    # length = len(PLAYlists)
    # for i in range(length):
    #     print(PLAYlists[i])

    status = cmd("mpc clear")
    sleep(0.1)
    # print(("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else ("mpc load " + PLAYlists[0]))
    # status = cmd("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else cmd("mpc load " + PLAYlists[0])
    status= cmd("mpc load " + PLAYlists[PLAYLIST_X])
    getstationlen()
    status= status.replace(" ", "\n")
    # display.frezeeDisplay(2)
    # myoled.displayfs(status, 16)
    interuptDisplay(2, 16,status)
    sleep(1)
    status = cmd("mpc play")
    # displaytooled(status)
    broadcast_message("info="+status)
    display.frezeeDisplay(3)


def getstationlen(): #get total playlist
    global T_LINES
    global TOQ
    global SWITCH_PLAYLIST
    status = subprocess.check_output("mpc playlist", shell=True)
    status =  status.decode("utf-8")
    if "radioislam" in status or "Rodja" in status:
        SWITCH_PLAYLIST = True
        print("SWITCH_PLAYLIST " + "True" if True else "False")
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
    # myoled.display(text, (0,0))
    display.display(text, (0,0))
    print("to display="+text)

getPlayState()
getstationlen()


TORESTART=False
def restart():
    global TORESTART
    if TORESTART is False:
        TORESTART=True
        # display.frezeeDisplay(8)
        # myoled.displayfs("press again\nto reload\nprogram", 16)
        interuptDisplay(8, 16, "press again\nto reload\nprogram")
    else:
        # display.frezeeDisplay(3)
        # myoled.displayfs("reload...", 16)
        interuptDisplay(3, 16, "reload...")
        sleep(1)
        os.execv(sys.executable, ['python'] + sys.argv)

def msleep(minutes):
    sleeptimer.startcdown(minutes)

def ok():
    global MIN_SLEEP
    global MIN_SLEEPV
    if MIN_SLEEP>0:
        # stimer.startcdown(MIN_SLEEPV)
        # os.system("/usr/bin/python startsleeper.py "+ str(MIN_SLEEPV))
        # display.display("starting sleep timer\n", True)
        # display.frezeeDisplay(3)
        # myoled.displayfs("starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes",15)
        interuptDisplay(3, 15, "starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes")
        broadcast_message("info=starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes")
        MIN_SLEEP=0
        sleeptimer.startcdown(MIN_SLEEPV)


def millis():
    return round(time.time() * 1000)


PREVMILL=0;

def secondy():
    global PREVMILL
    if millis() > (PREVMILL + 1000):
        print("second")
        PREVMILL= millis()



def processIR(irval):
    global EN_NEXMEDIA_R
    if irval== KR_YELLOW:
        EN_NEXMEDIA_R= not EN_NEXMEDIA_R
        # display.frezeeDisplay(3)
        # display.display("REMOTE control\n"+("unlocked" if EN_NEXMEDIA_R else "locked"), False)
        interuptDisplay(3, 0,"REMOTE control\n"+("unlocked" if EN_NEXMEDIA_R else "locked"))
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
            # display.display("player stopped", False)
            # display.frezeeDisplay(3)
            interuptDisplay(3, 0, "STOP")
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
            exitset(True)
    else:
        if irval[:2]=="41":
            # interuptDisplay(3,  unregistered key remote\nor this remote locked")
            # display.frezeeDisplay(3)
            # display.display("unregistered key remote\nor this remote locked", False)
            interuptDisplay(3, 0, "unregistered key remote\nor this remote locked")


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
        # display.display("player stopped", False)
        # display.frezeeDisplay(3)
        interuptDisplay(3, 0, "STOP")
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



def processIRw(irval):
    global REMOTES
    if REMOTES[1]["enable"] is False:
        # display.frezeeDisplay(2)
        # myoled.displayfs("remote locked", 16)
        processIRe(irval)
        return
    else:
        for i in range(len(KR_wNUM)):
            if irval == KR_wNUM[i][1]:
                clickNum(KR_wNUM[i][0])
                break
        if irval == KW_VOLUP:
            print("volume up")
            setVOL(True)
        elif irval == KW_VOLDOWN:
            setVOL(False)
        elif irval == KW_STUP:
            setSTATION(True)
        elif irval == KW_STDOWN:
            setSTATION(False)
        elif irval == KW_ENTER:
            global MIN_SLEEP
            if MIN_SLEEP>0:
                ok()
            else:
                print("enter")
                os.system("mpc toggle")
        elif irval == KW_PLAY:
            # global MIN_SLEEP
            if MIN_SLEEP>0:
                ok()
            else:
                print("play")
                os.system("mpc play")
        elif irval == KW_STOP:
            print("mute > stop")
            # display.display("player stopped", False)
            # display.frezeeDisplay(3)
            interuptDisplay(3, 0, "STOP")
            os.system("mpc stop")
        elif irval == KW_INPUT:
            print("mode > switch playlist")  # switch playlist
            switchPLAYLIST()
        elif irval == KW_SVOL:
            print("call > vol jump")  # start vol
            startVol()
        elif irval == KW_TEN:  # 10+
            print("ccall > ten+")
            startTenPos()
        elif irval == KW_POWER:  # 10+
            print("reboot")
            reboot()
        elif irval == KW_POWER:  # 10+
            print("get net data")
        elif irval == KW_SLEEP:
            startsetsleep()
        elif irval == KW_MUTE:
            restart()


def processIRe(irval):
    global REMOTES
    global GOTOSTATION
    if REMOTES[3]["enable"] is False:
        # display.frezeeDisplay(2)
        # myoled.displayfs("remote locked", 16)
        interuptDisplay(2, 10,"remote locked")
        return
    else:
        for i in range(len(KR_eNUM)):
            if irval == KR_eNUM[i][1]:
                clickNum(KR_eNUM[i][0])
                break
        if irval == KRE_VOLUP:
            print("volume up")
            setVOL(True)
        elif irval == KRE_VOLDOWN:
            setVOL(False)
        elif irval == KRE_STUP:
            setSTATION(True)
        elif irval == KRE_STDOWN:
            setSTATION(False)
        elif irval == KRE_OK:
            global MIN_SLEEP
            if MIN_SLEEP>0:
                ok()
            else:
                print("enter")
                interuptDisplay(3, 16, "PLAY/\nPAUSE")
                os.system("mpc toggle")
        elif irval == KRE_PLAY:
            # global MIN_SLEEP
            if MIN_SLEEP>0:
                ok()
            else:
                print("play")
                interuptDisplay(3, 16, "PLAY")
                os.system("mpc play")
        elif irval == KRE_STOP:
            print("mute > stop")
            # display.display("player stopped", False)
            # display.frezeeDisplay(3)
            interuptDisplay(3, 0, "STOP")
            os.system("mpc stop")
        elif irval == KRE_TV:
            print("mode > switch playlist")  # switch playlist
            switchPLAYLIST()
        elif irval == KRE_RECALL:
            print("call > vol jump")  # start vol
            startVol()
        elif irval == KRE_INFO:  # 10+
            print("ccall > ten+")
            startTenPos()
        elif irval == KRE_POWER:  # 10+
            print("reboot")
            reboot()
        elif irval == KRE_POWER:  # 10+
            print("get net data")
        elif irval == KRE_TIMER:
            startsetsleep()
        elif irval == KRE_MUTE:
            restart()
        elif irval == KRE_FAV:
            startPlistTo()
        elif irval == KRE_EXIT:
            exitset(True)
        elif irval==KRE_PAGEUP:
            # display.setPage(True)
            stationPage(True)
        elif irval==KRE_PAGEDOWN:
            stationPage(False)
            # display.setPage(False)
        elif irval==KRE_GOTO:
            GOTOSTATION=True



# ser = serial.Serial(
#         port='/dev/ttyS5', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
#         baudrate = 9600,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=0.1
# )


# print("start listening serial")


#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"), static_path = os.path.join(os.path.dirname(__file__), "static")
    )


def broadcast_message(message):
    # print("broadcast_message "+ message)
    # wsclient=w
    for client in WSHandler.clients:
        # client.write_message(message)
        # print ("bc ws")
        try:
            client.write_message(message)
        except Exception as e:
            print(f"error sending ws msg : {e}")
        # client.write_message("info="+message)


#
# SCOUNT=0
# prev_status=""
# def infinity():
#     # global SCOUNT
#     # SCOUNT +=1
#     # if SCOUNT == 10:
#     #     if display.getmenu() is True:
#     #         display.onmenu(False)
#     #     SCOUNT=0
#     global prev_status
#     status = subprocess.check_output("mpc current", shell=True).decode("utf-8").replace("\n","")
#     if status!=prev_status:
#         broadcast_message("info="+status)
#     prev_status=status
#     print(status)
#     threading.Timer(1, infinity).start()
#
# infinity()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print ("[HTTP](MainHandler) User Connected.")
        self.render("index.html")

    def post(self):
        value=""
        curlval=""
        try:
            value = self.get_argument('sleep')
            print("set sleep "+ value)
        except:
            print("skiping cause argument not contain " + value)
        try:
            curlval=self.get_argument('curl')
            print("play c url "+ curval)
        except:
            print("skiping cause argument not contain " + curlval)
        if value !="":
            global MIN_SLEEPV
            MIN_SLEEPV = int(value)
            sleeptimer.startcdown(MIN_SLEEPV)
            # os.system("/usr/bin/python startsleeper.py "+ str(MIN_SLEEPV))
            # display.display("starting sleep timer\n", True)
            # display.frezeeDisplay(3)
            # myoled.displayfs("starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes",15)
            interuptDisplay(3 ,15 ,"starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes")
        if curlval!="":
            sleeptimer.resetas()
            global PLAY_CURL
            if PLAY_CURL is False:
                status = cmd("mpc clear")
            sleep(0.1)
            status = cmd("mpc add " + curlval)
            # display.frezeeDisplay(2)
            # myoled.displayfs(status, 16)
            interuptDisplay(2, 16,status)
            sleep(1)
            status = cmd("mpc play")
            displaytooled(status)
            broadcast_message("info="+status)
            display.frezeeDisplay(3)
            PLAY_CURL=True
            self.render("index.html")
            # pass
        # ok()
        # self.render("index.html")
class SettingHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("settings.html")
    def post(self):
        global REMOTES
        global CONFIGDATA
        try:
            data = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.set_status(400)  # Bad Request
            self.write({"error": "Invalid JSON"})
            return


        # value=self.get_argument('jremote')
        print("got post jremote")
        # REMOTES=data
        # CONFIGDATA['remote']=REMOTES
        REMOTES=CONFIGDATA.get("remote","")
        print("remote array: "+ str(REMOTES))
        CONFIGDATA=data
        j=json.dumps(data)
        print(j)
        with open(file_path, "w") as f:
            json.dump(CONFIGDATA, f)


class shellCmd(tornado.web.RequestHandler):#scmd
    def get(self,input):
        # print("input="+str(input))
        # cmd=self.get_argument('hostname')
        if input=="playlist":
            idd=0
            if (getPlayState()) is True:
                idd=int(subprocess.check_output("mpc -f [%position%] | awk 'NR==1 {print}'",shell=True).decode("utf-8"))
            sr=subprocess.check_output("mpc playlist", shell=True).decode("utf-8")
            pl=sr.splitlines(keepends=False)
            rp=""
            for i in range(len(pl)):
                if "://" in pl[i]:
                    pl[i]=pl[i][pl[i].index("//")+2:]
                if i+1==idd:
                    rp+= "<button id=\"playing\" class=\"button1 bplay\" onclick=\"sendcmd('mpc play " + str(i+1) +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
                else:
                    rp+= "<button class=\"button1\" onclick=\"sendcmd('mpc play " + str(i+1) +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
            self.write(rp)
        elif input== "iplaylist":
            sr=subprocess.check_output("mpc lsplaylists", shell=True).decode("utf-8")
            pl=sr.splitlines(keepends=False)
            rp=""
            for i in range(len(pl)):
                rp+= "<button class=\"button1\" onclick=\"sendcmd('mpc load " + pl[i] +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
            self.write(rp)
        elif input== "status":
            sr=subprocess.check_output("mpc", shell=True).decode("utf-8")
            self.write(sr)
        elif input== "config":
            global CONFIGDATA
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(CONFIGDATA))
        elif input== "remotes":
            global REMOTES
            rp=""
            for i in range(len(REMOTES)):
                #rp+= "<button class=\"button1\" onclick=\"sendcmd('mpc play " + str(i+1) +"')\"><a>"+str(i+1)+". "+str(REMOTES[i]["name"])+"</a></button>"
                benable= "" if REMOTES[i]["enable"] is False else "checked=\"true\""
                # rp+="<div id=\"state1\" class=\"switch_led\" style=\"margin: auto; padding: 8px\" ><p4 id=\"swp1\" style=\"font-size: 12px\">"+ str(i+1) + ". "+str(REMOTES[i]["name"]) +"</p4><label class=\"switchled\"> <input type=\"checkbox\" checked=\""+str(REMOTES[i]["enable"]) +"\" id=\"remote"+str(i+1)+"\" onchange=\"rchange("+ str(i+1)+")\"/> <span class=\"slider\"></span></label> </div>"
                rp+="<div id=\"state1\" class=\"switch_led\" style=\"margin: auto; padding: 8px\" ><p4 id=\"swp1\" style=\"font-size: 12px\">"+ str(i+1) + ". "+str(REMOTES[i]["name"]) +"</p4><label class=\"switchled\"> <input type=\"checkbox\" "+ benable +" id=\"remote"+str(i+1)+"\" value=\""+str(REMOTES[i]["name"]) +"\" onchange=\"rchange("+ str(i+1)+")\"/> <span class=\"slider\"></span></label> </div>"

                # rp+="<div id=\"state1\" class=\"switch_led\" style=\"margin: auto; padding: 8px\" ><p4 id=\"swp1\" style=\"font-size: 12px\">"+ str(i+1) + ". "+str(REMOTES[i]["name"]) +"</p4><label class=\"switchled\"> <input type=\"checkbox\" checked=false id=\"remote"+str(i+1)+"\" onchange=\"rchange("+ str(i+1)+")\"/> <span class=\"slider\"></span></label> </div>"

            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(REMOTES))
        elif input== "hostname":
            sr=subprocess.check_output("hostname", shell=True).decode("utf-8")
            self.write(sr)
        elif input== "getsleep":
            sst=sleeptimer.update()
            self.write(sst)
        elif input== "stopsleep":
            sst=sleeptimer.stopcdown()
            self.write("timer stopped")
        elif input == "restart":
            print("This program will restart itself in 2 seconds...")
            interuptDisplay(8, 0, "Restarting app")
            time.sleep(0.5)  # Wait for 5 seconds before restarting
            # Restart the program
            print("Restarting...")
            # self.render("webscr.html", wsurl=urll, tms=_TS)
            rp = 'app restarting'
            self.write(rp)
            time.sleep(1.5)
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            self.write("command not recognized")
    def post(self):
        value = self.get_argument('cmd')
        sr=subprocess.check_output("mpc volume "+ value, shell=True).decode("utf-8")
        self.write("volume"+sr)
        # print(cmd)

# WebSocket handler
class WSHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    def open(self):
        # print("WebSocket opened by ")
        # print(f"Client connected: {self.request.remote_ip}")
        remote_ip = self.request.remote_ip
        try:
            hostname, _, _ = socket.gethostbyaddr(remote_ip)
            print(f"WebSocket opened from {hostname} ({remote_ip})")
        except socket.herror:
            print(f"WebSocket opened from {remote_ip} (hostname not resolved)")
        self.clients.add(self)

    def on_close(self):
        print("WebSocket closed")
        self.clients.remove(self)

    def on_message(self, message):
        print (f'[WS] Incoming message:{message}'), message

        if message.startswith("0>"):
            sbmsg=message[2:]
            if sbmsg.startswith("mpc"):
                sleeptimer.resetas()
                print("start with mpc")
            if sbmsg.startswith("mpc load"):
                subprocess.check_output("mpc clear", shell=True)
                subprocess.check_output(sbmsg, shell=True).decode("utf-8")
                subprocess.check_output("mpc play ", shell=True).decode("utf-8")
                global PLAY_CURL
                PLAY_CURL=False
                interuptDisplay(3, 16, "switcing PLAYlists")
            elif sbmsg.startswith("mpc volume"):
                out= subprocess.check_output(sbmsg + " | grep volume | awk '{print$2}'", shell=True).decode("utf-8")
                # display.frezeeDisplay(3)
                # display.displayfs("v "+out, 25)
                interuptDisplay(3, 25,"v "+out)

            else:
                sr=subprocess.check_output(sbmsg, shell=True).decode("utf-8")
                print("incoming ws msg: " + sr)
                interuptDisplay(3, 16, sr)
        elif message.startswith("1>"):
            sbmsg=message[2:]
            if sbmsg.startswith("stopsleep"):
                sleeptimer.stopcdown()
    @classmethod
    async def send_message(cls, message):
        for client in cls.clients:
            if client.ws_connection:  # Check if the client is still connected
                try:
                    await client.write_message(message)
                except Exception as e:
                    print(f"error sending ws msg : {e}")

# Serial reader
class SerialReader(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Serial port opened", transport)

    def data_received(self, data):
        message = data.decode('utf-8').strip()
        print(f"Received from serial: {message}")
        ss=message[:2]
        if ss == "FF":
            processIRc(message)
            sleeptimer.resetas()
        elif ss == "41":
            processIR(message)
            sleeptimer.resetas()
        elif ss == "FD":
            processIRw(message)
            sleeptimer.resetas()
            # print (s)
        # asyncio.create_task(WSHandler.send_message(message))#echoing

    def connection_lost(self, exc):
        print("Serial port closed")
        asyncio.get_event_loop().stop()

async def start_serial_reader(port, baudrate):
    loop = asyncio.get_event_loop()
    await serial_asyncio.create_serial_connection(loop, SerialReader, port, baudrate)

# Tornado application setup
def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/scmd/(\w+)', shellCmd),
        (r"/websocket", WSHandler),
        (r"/settings", SettingHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"})
    ],
        **settings)

def sleepCountDown():
    global RADIOSLEEPTIMERENABLED
    global RADIOSECONDSLEEPTIMER
    global USERSLEEPTIMERENABLED
    global USERSECONDSLEEPTIMER

    if RADIOSLEEPTIMERENABLED is True:
        RADIOSECONDSLEEPTIMER-=1
        if RADIOSECONDSLEEPTIMER==0:
            RADIOSLEEPTIMERENABLED=False
            status=int(subprocess.check_output("mpc stop",shell=True).decode("utf-8"))
            broadcast_message("player stop cause inactive control over than 1 hour")

    if USERSLEEPTIMERENABLED is True:
        USERSECONDSLEEPTIMER-=1
        if USERSECONDSLEEPTIMER==0:
            USERSLEEPTIMERENABLED=False
            status=int(subprocess.check_output("mpc stop",shell=True).decode("utf-8"))
            broadcast_message("player stop cause set by user")




SCOUNT=0
prev_status=""
prev_plist=""

def broadcast_rplist():
    global prev_plist
    idd=0
    if (getPlayState()) is True:
        idd=int(subprocess.check_output("mpc -f [%position%] | awk 'NR==1 {print}'",shell=True).decode("utf-8"))
    sr=subprocess.check_output("mpc playlist", shell=True).decode("utf-8")
    pl=sr.splitlines(keepends=False)
    rp=""
    for i in range(len(pl)):
        if "://" in pl[i]:
            pl[i]=pl[i][pl[i].index("//")+2:]
        if i+1==idd:
            rp+= "<button id=\"playing\" class=\"button1 bplay\" onclick=\"sendcmd('mpc play " + str(i+1) +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
        else:
            rp+= "<button class=\"button1\" onclick=\"sendcmd('mpc play " + str(i+1) +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
    if rp!=prev_plist:
        prev_plist=rp
        broadcast_message("pls="+rp)
#
#         try:
#             print("broadcast playlist")
#             broadcast_message("pls="+rp)
#         except:
#             print("error")



def infinity():
    global SCOUNT
    SCOUNT +=1
    if SCOUNT % 2==0:
        broadcast_rplist()
    if SCOUNT == 10:
        SCOUNT=0
    # sleepCountDown()
    global prev_status
    status = subprocess.check_output("mpc current", shell=True).decode("utf-8").replace("\n","")
    if status!=prev_status:
        try:
            broadcast_message("info="+status+">__ws")
        except Exception as e:
            print(f"error sending ws msg : {e}")
    prev_status=status
    # print(status)
    threading.Timer(1, infinity).start()
def signal_handler(sig, frame):
    print("Signal received, cancelling tasks...")
    for task in asyncio.all_tasks():
        task.cancel()

#infinity()
async def iorun():
    # Start the serial reader
    asyncio.ensure_future(start_serial_reader(port, baudrate))

    # Start the Tornado I/O loop
    tornado.ioloop.IOLoop.current().start()
    loop.add_signal_handler(signal.SIGINT, signal_handler)

# if __name__ == "__main__":
port = '/dev/ttyS5'  # Change this to your serial port
baudrate = 9600  # Change this to your desired baudrate

app = make_app()
app.listen(8888)
mtimer.start()
try:
    # Start the serial reader
    asyncio.ensure_future(start_serial_reader(port, baudrate))

    # Start the Tornado I/O loop
    tornado.ioloop.IOLoop.current().start()
    asyncio.run(iorun())
except KeyboardInterrupt:
    mtimer.stop()
    sleep(1)
    print("Keyboard interrupt received, exiting...")



#
# while True:
#     x=ser.readline()
#     s=x.decode("utf-8")
#     ss=s[:2]
#     if ss == "FF":
#         processIRc(s)
#     elif ss == "41":
#         processIR(s)
#         # print (s)
#     # print ("ss="+ss)
#     sleep(0.01)
#     # except:
#     # print("device failed")
# else:
#     os.exit(0)
