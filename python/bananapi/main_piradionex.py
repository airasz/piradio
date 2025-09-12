#!usr/bin/env python
# import RPi.GPIO as GPIO
import time
import evdev
from evdev import InputDevice, categorize, ecodes
import os
import sys
from time import sleep
import socket
import json
import subprocess
import asyncio
import threading
import re

# from evdev import InputDevice

# import mpcstimer
# import serialdisplay

import module_piradionex
from module_piradionex import get_mpc_status

# from python.orangepi.main_radio import CONFIGDATA
# from python.orangepi.module_radio import ASSECCD

display = module_piradionex.display()
mtimer = module_piradionex.tasktimer()

import tornado
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


# stimer=mpcstimer.mpctimer()
sleeptimer = module_piradionex.sleeptimer()  # used as sleep timer

SWITCH_PLAYLIST = False
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0
DBG_EVENT = False
EN_NEXMEDIA_R = True

PLAY_CURL = False
PLAYLIST_X = 0

saved_eval = 0

SCOUNT = 0


VOLTO = 0
CONFIGDATA = {}
GOTOSTATION = False
# remot key nexmedia
KR_POWER = 2099200
KR_OPT = 2099287
KR_D_UP = 2099218
KR_D_DOWN = 2099219
KR_VOLUP = 2099202
KR_VOLDOWN = 2099203
KR_STUP = 2099206
KR_STDOWN = 2099207
KR_GREEN = 2099225
KR_OK = 2099221
KR_SLEEP = 2099231
KR_EXIT = 2099216
KR_MEDIA = 2099290
KR_FORWARD = 2099275
KR_REVERSE = 2099272
KR_INFO = 2099280
KR_NUMKEYS = [
    [1, 2099228],
    [2, 2099229],
    [3, 2099230],
    [4, 2099264],
    [5, 2099265],
    [6, 2099266],
    [7, 2099268],
    [8, 2099269],
    [9, 2099270],
    [10, 2099271],
]
KB_NUMKEYS = [
    [1, 458841],
    [2, 458842],
    [3, 458843],
    [4, 458844],
    [5, 458845],
    [6, 458846],
    [7, 458847],
    [8, 458848],
    [9, 458849],
    [10, 458850],
]

# KB_NUMKEYS=[[1 , KEY_KP1],[2 , KEY_KP2],[3 , KEY_KP3],[4 , KEY_KP4],[5 , KEY_KP5],[6 , KEY_KP6],[7 , KEY_KP7],[8 , KEY_KP8],[9 , KEY_KP9],[10 , KEY_KP0]]

stationAlternative = {"My Station name": "Hang FM Batam"}
# temporary flag
TEN = False
NUM_VOL = 0
TO_REBOOT = False
HASINTERNET_ = False
MIN_SLEEP = 0
MIN_SLEEPV = 0
T_LINES = 0
TOQ = 0
TS_ENABLE = False
STOP_SLEEP = 0
drawPlayListMode = 0

PLAYlists = []
splited_playlist = []
splited_playlist_pointer = 0
splp = False


pulse_ = 0
secondDigit = 0

VOLUME_UP = 115
VOLUME_DOWN = 114

NEXT = 163
PREV = 165
PLAY = 164
STOP = 166
# SWITCH_PLAYLIST = True
# MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0
T_LINES = 0
# TEN = False
# TOQ=0

NUMKEYS = [
    [1, 79],
    [2, 80],
    [3, 81],
    [4, 75],
    [5, 76],
    [6, 77],
    [7, 71],
    [8, 72],
    [9, 73],
    [10, 82],
]

config_path = "radioconfig.json"


def interuptDisplay(delay, msg):
    display.frezeeDisplay(delay)
    display.display(msg, False)


def load_variable():
    global CDOWN
    global TS_ENABLE
    try:
        with open("timer.json", "r") as f:
            data = json.load(f)
            TS_ENABLE = data.get("enable", False)
    except FileNotFoundError:
        pass


def save_config():
    global CONFIGDATA
    with open(config_path, "w") as f:
        json.dump(CONFIGDATA, f, indent=4)


def cmd(cmd):
    rtr = ""
    try:
        rtr = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        rtr = e.output
        # rtr="eror"

    rtr = rtr.decode("utf-8")
    return rtr


def noReturnSubprocess(cmd):
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("error in cmd: " + cmd)
        print(e.output.decode("utf-8"))


def dividePlayList():
    global splited_playlist
    # display.frezeeDisplay(50)
    sr = subprocess.check_output("mpc playlist", shell=True).decode("utf-8")
    pl = [f"{index}. {line}" for index, line in enumerate(sr.splitlines(), start=1)]
    chunk_size = 10
    splited_playlist = [pl[i : i + chunk_size] for i in range(0, len(pl), chunk_size)]
    # print(split_list)
    # for item in split_list:
    # print(item)

    # display.sendCommand(f't1.txt="{rp}"')


def loadPLAYlists():
    global PLAYlists
    # status = cmd("ls /var/lib/mpd/playlists/")
    # status = status.replace(".m3u", "")
    # PLAYlists = status.split()
    sr = subprocess.check_output("mpc lsplaylists", shell=True).decode("utf-8")
    PLAYlists = sr.splitlines(keepends=False)
    dividePlayList()
    # print(f'playlist no 2:{PLAYlists[1]}')


loadPLAYlists()


def hasInsternet():
    print("check Internet Connection")
    global HASINTERNET_
    try:
        s = socket.create_connection(("www.google.com", 80))
        if s is not None:
            s.close
        HASINTERNET_ = True
        return
    except OSError:
        pass
    HASINTERNET_ = False
    return


while HASINTERNET_ is False:
    hasInsternet()


# get total queue
def getTotalQ():
    # status = "radio volume: 50%"
    # os.system("mpc playlist > tmp")
    # status = open("tmp", "r").read()
    # tq = status.count("\n") + 1
    tq = int(cmd("mpc playlist | wc -l"))
    global SWITCH_PLAYLIST

    # if "muslim" in status:
    # print("playlist muslim detected")
    # SWITCH_PLAYLIST = False
    # if tq < 10:
    #     SWITCH_PLAYLIST = True
    # print("total queue = " + str(tq))
    return tq


# os.system("mpc volume 50")
os.system("ir-keytable -p nec")
# os.system("/usr/bin/mpc play")
TOQ = getTotalQ()


# os.system("/usr/bin/python3 mpcsleeper.py")
def getVol():
    # status = subprocess.check_output("mpc volume | grep volume | awk '{print$2}'",shell=True).decode("utf-8").replace("%","")
    status = cmd("mpc status | grep -o 'volume: [0-9]\+' | sed 's/volume: //'")
    # status=mpc("mpc status | awk '/volume:/ {for(i=1;i<=NF;i++) if($i ~ /^volume:/) print substr($i,8)}'")
    # print("s="+status )
    vol = int(status)
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
    status = ""
    status = cmd("mpc")

    if "playing" in status:
        return True
    elif "paused" in status:
        return True
    else:
        return False


def playToggle():
    # os.system("mpc "+ ("stop" if getPlayState() else "play"))
    noReturnSubprocess(f'mpc {("stop" if getPlayState() else "play")}')


def setVOL(up):
    status = ""
    vol = ""
    # status = subprocess.check_output(("mpc volume +5 | grep volume | awk '{print$2}'") if up else ("mpc volume -5 | grep volume | awk '{print$2}'"), shell=True).decode("utf-8")
    status = cmd(
        "mpc volume " + ("+5" if up else "-5") + " | grep volume | awk '{print$2}'"
    )
    print("vol " + status)
    interuptDisplay(3, "set volume " + status)


def trackrepeat():
    RESULT = cmd("mpc repeat | grep -o 'repeat: \w\+' | awk '{print $2}'")  # toggle
    interuptDisplay(3, 15, "repeat " + RESULT)


def seekthrough(forward):
    status = ""
    vol = ""
    # status = subprocess.check_output(("mpc volume +5 | grep volume | awk '{print$2}'") if up else ("mpc volume -5 | grep volume | awk '{print$2}'"), shell=True).decode("utf-8")
    status = cmd("mpc seekthrough " + ("+1:00" if forward else "-1:00"))
    print("vol " + status)
    # interuptDisplay(3, "set volume "+ status)


def setSTATION(next):
    if (getPlayState()) is True:
        interuptDisplay(3, "playing next" if next else "playing previous")
        # os.system("mpc "+ ("next" if next else "prev"))
        noReturnSubprocess(f'mpc {("next" if next else "prev")}')


def getCurrentStation():  # return  pos
    cs = ""

    # status = "radio volume: 50%"
    # status = subprocess.check_output("mpc", shell=True)
    # status =  status.decode("utf-8")
    # ps = status.index(']')
    # pps=status.index('%')
    # pss=status[ps:pps]
    # ht=pss.index("#")
    # fs=pss.index('/')
    # cs=pss[ht+1:fs]

    cs = cmd("mpc status | grep -o '#[0-9]\+' | sed 's/#//'")
    # cs=cmd("mpc -f %position%")

    return int(cs)


def stationPage(next):
    global TOQ
    status = ""
    cs = getCurrentStation()
    if next:
        cs = cs + 10
        if cs > TOQ:
            cs = TOQ
        interuptDisplay(2, "play pos " + str(cs))
        noReturnSubprocess(f"mpc play {cs}")
        # status = subprocess.check_output(f"mpc play {cs}", shell=True)
        # status =  status.decode("utf-8")
    else:
        cs = cs - 10
        if cs < 1:
            cs = 1
        interuptDisplay(2, "play pos " + str(cs))
        noReturnSubprocess(f"mpc play {cs}")
        # status = subprocess.check_output(f"mpc play {cs}", shell=True)
        # status =  status.decode("utf-8")


def reboot():
    global TO_REBOOT
    if TO_REBOOT is False:

        TO_REBOOT = True
        interuptDisplay(1, "press again to reboot")

    else:
        interuptDisplay(1, "rebooting...")
        sleep(1)
        os.system("reboot")


def playPos(pos):
    global TEN
    global VOLTO
    global NUM_VOL
    global MIN_SLEEP
    global MIN_SLEEPV
    global splp
    global secondDigit
    global pulse_
    status = ""

    pulse_ = 0
    # display.display("volume to "+ str(pos + 10 if TEN else pos))
    if NUM_VOL == 0 and MIN_SLEEP == 0 and splp is False:
        # display.display("play pos "+ str(pos), True)
        # display.frezeeDisplay(3)
        # myoled.displayfs("play pos "+ str(pos),15)
        if TOQ < 10:
            interuptDisplay(3, "play pos " + str(pos))
            # os.system("mpc play " + str(pos))
            noReturnSubprocess(f"mpc play {pos}")
            exitset(False)

            return
        else:
            if secondDigit > 0:
                secondDigit += pos
                if secondDigit > TOQ:
                    interuptDisplay(
                        3, "input out range\n" + (f"{secondDigit} in {TOQ}")
                    )
                    secondDigit = 0
                    exitset(False)
                    return
                else:
                    interuptDisplay(3, "play pos " + str(secondDigit))
                    noReturnSubprocess(f"mpc play {secondDigit}")
                    # os.system("mpc play " + str(secondDigit))
                    secondDigit = 0
                    broadcast_message("resettimer")
                exitset(False)
                return
            else:
                interuptDisplay(3, (f"play pos {str(pos)}_"))
                secondDigit = pos * 10
                exitset(False)
                return

            # os.system("mpc play " + str(pos))
        return

        # interuptDisplay(3, "play pos "+ str(pos))
        # os.system("mpc play " + str(pos))
        # exitset(False)
        # return
    if NUM_VOL == 1:
        VOLTO = pos * 10
        interuptDisplay(5, "volume to " + str(pos) + "x")
        print("start vol========== " + str(VOLTO))
        NUM_VOL = 2
    elif NUM_VOL == 2:
        VOLTO += pos
        NUM_VOL = 0
        interuptDisplay(5, "volume to " + str(VOLTO))
        # os.system("mpc volume " + str(VOLTO))
        noReturnSubprocess(f"mpc volume {VOLTO}")
        exitset(False)

    if MIN_SLEEP == 1:
        # MIN_SLEEPV+=pos**MIN_SLEEP
        MIN_SLEEPV = 0
        MIN_SLEEPV = pos * 10
        interuptDisplay(5, "sleep in " + str(pos) + "x minutes")
        #
        MIN_SLEEP = 2
    elif MIN_SLEEP == 2:
        MIN_SLEEPV += pos
        interuptDisplay(
            5, "sleep in " + str(MIN_SLEEPV) + " minutes\nClick OK to confirm"
        )
    if splp is True:
        # status = cmd("mpc clear")
        noReturnSubprocess("mpc clear")
        sleep(0.1)
        if pos < len(PLAYlists) + 1:
            status = cmd("mpc load " + PLAYlists[pos - 1])
            getstationlen()
            status = status.replace(" ", "\n")
            interuptDisplay(1, status)
            sleep(0.6)
            # status = cmd("mpc play")
            noReturnSubprocess("mpc play")
            sleep(0.4)
            status = cmd("mpc current")
            if status in stationAlternative:
                status = stationAlternative[status]
            interuptDisplay(1, status)
        loadPLAYlists()
        splp = False


def startVol():
    global NUM_VOL
    exitset(False)
    NUM_VOL = 1
    interuptDisplay(1, "jump volume to...")
    # display.onmenu(True)


def startTenPos():
    global TEN
    global NUM_VOL
    exitset(False)
    TEN = True

    interuptDisplay(2, "set play pos 1...")
    # display.onmenu(True)


def startsetsleep():
    global stimerStop
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    global STOP_SLEEP
    load_variable()
    # display.onmenu(True)
    if TS_ENABLE is True:
        if STOP_SLEEP == 0:
            STOP_SLEEP += 1
            interuptDisplay(5, "press again to stop")
        else:
            jdata = {"enable": False, "startrun": False, "svalue": 0, "seconds": 0}
            with open("timer.json", "w") as f:
                json.dump(jdata, f)
            interuptDisplay(5, "sleep timer stopped")

            STOP_SLEEP = 0
    else:
        interuptDisplay(8, "set sleep...")
        exitset(False)
        MIN_SLEEP = 1


def startPlistTo():
    global splp
    global PLAYlists
    exitset(False)
    splp = True
    pls = ""
    ids = 0
    dbl = 0
    PLAYlists.sort()
    for item in PLAYlists:
        dbl += 1
        # print(f'{str(ids+1)}. {str(item)}\n')
        if dbl % 3 == 0:
            pls += f"{str(ids+1)}. {str(item)}\n"
        else:
            pls += f"{str(ids+1)}. {str(item)}  "
        ids += 1
    # display.frezeeDisplay(8)
    # display.display(f'select.\n{pls}', False)
    interuptDisplay(2, (f"select.\n{pls}"))


def ok():
    global MIN_SLEEP
    global MIN_SLEEPV
    if MIN_SLEEP > 0:
        # stimer.startcdown(MIN_SLEEPV)
        # os.system("/usr/bin/python3 startsleeper.py "+ str(MIN_SLEEPV))
        interuptDisplay(5, "sleep timer starting for " + str(MIN_SLEEPV) + " minutes")
        MIN_SLEEP = 0
        sleeptimer.startcdown(MIN_SLEEPV)
        exitset(False)
    else:
        noReturnSubprocess("mpc toggle")
        # if getPlayState():
        #     noReturnSubprocess("mpc toggle")


def exitset(info):
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    global STOP_SLEEP
    global MIN_SLEEPV
    global TO_REBOOT
    global splp
    global GOTOSTATION
    global splited_playlist_pointer
    GOTOSTATION = False
    TO_REBOOT = False
    splp = False
    TEN = False
    NUM_VOL = 0
    STOP_SLEEP = False
    MIN_SLEEP = 0
    # display.onmenu(False)
    if splited_playlist_pointer > 0:
        splited_playlist_pointer = 0
        display.sendCommand("page page4")
        display.sendCommand('t0.txt="banana radio"')
        display.resettimer()

    if info:
        interuptDisplay(2, "start set resetted")


def getstationlen():  # get total playlist
    global T_LINES
    global TOQ
    global SWITCH_PLAYLIST
    # status = subprocess.check_output("mpc playlist", shell=True)
    # status =  status.decode("utf-8")
    status = cmd("mpc playlist")
    if "muslim" in status:
        SWITCH_PLAYLIST = False
    T_LINES = status.count("\n")
    TOQ = T_LINES
    print("playlist=" + str(T_LINES))
    # print(T_LINES)


def switchPLAYLIST():
    global SWITCH_PLAYLIST
    global PLAYLIST_X
    global PLAYlists
    # global PLAYlists
    # SWITCH_PLAYLIST = not SWITCH_PLAYLIST
    getstationlen()
    if SWITCH_PLAYLIST is True:
        SWITCH_PLAYLIST = False
    else:
        SWITCH_PLAYLIST = True

    print("SWITCH_PLAYLIST=" + str(SWITCH_PLAYLIST))
    # import os

    # status = os.popen("ls /var/lib/mpd/playlists/").read()
    # status = cmd("ls /var/lib/mpd/playlists/")
    # status = status.replace(".m3u", "")
    # PLAYlists = status.split()

    # PLAYLIST_X.sort()
    PLAYLIST_X += 1
    if PLAYLIST_X == len(PLAYlists):
        PLAYLIST_X = 0

    status = cmd("mpc clear")
    sleep(0.1)
    # status= cmd("mpc load " + PLAYlists[PLAYLIST_X])
    noReturnSubprocess(f"mpc load {PLAYlists[PLAYLIST_X]}")
    getstationlen()

    interuptDisplay(2, status)
    sleep(1)
    # status = cmd("mpc play")
    noReturnSubprocess("mpc play")


def drawPlayList():
    global splited_playlist
    global splited_playlist_pointer
    global TOQ
    display.frezeeDisplay(50)
    rp = ""
    prange = ""
    splited_playlist_pointer += 1
    if splited_playlist_pointer < len(splited_playlist) + 1:
        if splited_playlist_pointer < len(splited_playlist):
            prange = f"{(splited_playlist_pointer*10)-10+1} - {(splited_playlist_pointer*10)}"
        else:
            prange = f"{(splited_playlist_pointer*10)-10+1} - {TOQ}"
        rp = "\n".join(splited_playlist[splited_playlist_pointer - 1])
        print(rp)
        rp = rp.replace("https://", "").replace("http://", "")
        if splited_playlist_pointer == 1:
            display.sendCommand("page page6")
        display.setPage(1)
        display.sendCommand(f't0.txt="playlist ({prange}) {TOQ}"')
        display.sendCommand(f't1.txt="{rp}"')
        # for item in splited_playlist[splited_playlist_pointer]:
        # rp
    else:
        splited_playlist_pointer = 0
        display.setPage(1)
        display.sendCommand("page page4")
        display.sendCommand('t0.txt="banana radio"')


# elif drawPlayListMode> 0:
#         drawPlayListMode=0
#         display.sendCommand('page page4')


def processIR(irval):
    global EN_NEXMEDIA_R
    global GOTOSTATION
    print(irval)
    # display.resettimer()
    # hexval = hex(irval)
    # print(hexval)
    # sval=str(irval)
    #
    # display.resettimer(sval)
    # interuptDisplay(sval)
    if irval == KR_GREEN:
        EN_NEXMEDIA_R = not EN_NEXMEDIA_R
        interuptDisplay(
            3, "REMOTE control " + ("unlocked" if EN_NEXMEDIA_R else "locked")
        )
        # if EN_NEXMEDIA_R if False:
        #     interuptDisplay(5, "REMOTE control unlocked")
        # else:
        #     interuptDisplay(5, "REMOTE control unlocked")
        return

        # print
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
            # os.system("mpc play")
            noReturnSubprocess("mpc play")
        elif irval == 2099267:
            print("pause")
            noReturnSubprocess("mpc pause")
        elif irval == 2099277:
            print("stop")
            interuptDisplay(3, "stop player")
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
        elif irval == KR_SLEEP:
            # msleep(20)
            startsetsleep()
        elif irval == KR_OK:
            ok()
        elif irval == KR_EXIT:
            exitset(True)
        elif irval == KR_MEDIA:
            startPlistTo()
        elif irval == KR_FORWARD:
            stationPage(True)
        elif irval == KR_REVERSE:
            stationPage(False)
        elif irval == KR_INFO:
            drawPlayList()
        elif irval == 2099274:
            seekthrough(True)
        elif irval == 2099273:
            seekthrough(False)

    else:
        if irval > 2000000:
            interuptDisplay(5, "unregistered key remote\nor this remote locked")


def processKB(kval):
    print("processKB" + str(kval))
    for i in range(len(KB_NUMKEYS)):
        # NKV=int(KR_NUMKEYS[i][1])
        # NKI=int (KR_NUMKEYS[i][0])
        if kval == KB_NUMKEYS[i][1]:
            playPos(KB_NUMKEYS[i][0])
            break


def processKboard(ecode):
    sleeptimer.resetas()
    if ecode == VOLUME_UP:
        setVOL(True)
    if ecode == VOLUME_DOWN:
        setVOL(False)
    if ecode == NEXT:
        setSTATION(True)
    if ecode == PREV:
        setSTATION(False)
    if ecode == PLAY:
        # os.system("mpc play")
        noReturnSubprocess("mpc play")
        # status = cmd("mpc play")
        getPlayState()
    if ecode == STOP:
        interuptDisplay(3, "stop player")
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


async def OLD_print_events(device):
    async for event in device.async_read_loop():
        # print(device.path, evdev.categorize(event), sep=': ')
        # print(device.path, event.value, sep=': ')
        global saved_eval
        if event.value > 10:
            saved_eval = event.value
            if DBG_EVENT is True:
                print("saved_eval= " + str(saved_eval))

        if DBG_EVENT is True:
            print("ev_key= " + str(ecodes.EV_KEY))
            print("etype= " + str(event.type))
            print("ecode= " + str(event.code))
            print("evalue= " + str(event.value))
        if event.type == ecodes.EV_KEY:
            c = categorize(event)
            print("keystate= " + str(c.keystate))
            if c.keystate == c.key_down:
                if DBG_EVENT is True:
                    print(c.keycode)
            if event.value == 0:
                if DBG_EVENT is True:
                    print("keyboard typed")
                    print("KBev_key= " + str(ecodes.EV_KEY))
                    print("KBetype= " + str(event.type))
                    print("KBecode= " + str(event.code))
                processKB(saved_eval)
        else:
            print("processIR")
            processIR(event.value)

        # print(event.code)


def infinity():
    global SCOUNT
    SCOUNT += 1
    if SCOUNT == 10:
        # if display.getmenu() is True:
        #     display.onmenu(False)
        SCOUNT = 0

    # threading.Timer(1, infinity).start()


# infinity()


async def print_events(device):
    async for event in device.async_read_loop():
        # print(device.path, evdev.categorize(event), sep=': ')
        # print(device.path, event.value, sep=': ')
        global saved_eval

        if event.value > 200000:
            saved_eval = event.value
            if DBG_EVENT is True:
                print("saved_eval= " + str(saved_eval))

        if DBG_EVENT is True:
            print("ev_key= " + str(ecodes.EV_KEY))
            print("etype= " + str(event.type))
            print("ecode= " + str(event.code))
            print("evalue= " + str(event.value))
            print(categorize(event))
        if event.type == ecodes.EV_KEY:
            c = categorize(event)
            print("keystate= " + str(c.keystate))
            if c.keystate == c.key_up:  # 0=up, 1=hold, 2=down
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
        if event.value > 2000000:
            sleeptimer.resetas()
        if DBG_EVENT is True:
            print("===============end debug==========")
        # print(event.code)


# for device in ir, keybd:
# asyncio.ensure_future(print_events(device))


# Tornado Folder Paths
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


def broadcast_message(message):
    print("broadcast_message " + message)
    for client in WSHandler.clients:
        client.write_message(message)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("[HTTP](MainHandler) User Connected.")
        self.render("index.html")

    def post(self):
        value = ""
        curlval = ""
        try:
            value = self.get_argument("sleep")
            print("set sleep " + value)
        except:
            print("skiping cause argument not contain " + value)
        try:
            curlval = self.get_argument("curl")
            print("play c url " + curlval)
        except:
            print("skiping cause argument not contain " + curlval)
        if value != "":
            global MIN_SLEEPV
            MIN_SLEEPV = int(value)
            sleeptimer.startcdown(MIN_SLEEPV)
            # os.system("/usr/bin/python startsleeper.py "+ str(MIN_SLEEPV))
            # display.display("starting sleep timer\n", True)
            # display.frezeeDisplay(3)
            # myoled.displayfs("starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes",15)
        if curlval != "":
            # stimer.resetas()
            global PLAY_CURL
            if PLAY_CURL is False:
                # status = cmd("mpc clear")
                noReturnSubprocess("mpc clear")
            sleep(0.1)
            noReturnSubprocess("mpc add " + curlval)
            sleep(1)
            status = cmd("mpc play")
            save_config()
            broadcast_message("info=" + status)
            PLAY_CURL = True
            # pass
        # ok()
        self.render("index.html")


class shellCmd(tornado.web.RequestHandler):  # scmd
    def get(self, input):

        global PLAYlists
        # print("input="+str(input))
        # cmd=self.get_argument('hostname')
        if input == "playlist":
            idd = 0
            if (getPlayState()) is True:
                idd = int(
                    subprocess.check_output(
                        "mpc -f [%position%] | awk 'NR==1 {print}'", shell=True
                    ).decode("utf-8")
                )
            sr = subprocess.check_output("mpc playlist", shell=True).decode("utf-8")
            pl = sr.splitlines(keepends=False)

            rp = ""
            for i in range(len(pl)):
                if pl[i] in stationAlternative:
                    pl[i] = stationAlternative[pl[i]]
                if "://" in pl[i]:
                    pl[i] = pl[i][pl[i].index("//") + 2 :]
                if i + 1 == idd:
                    rp += (
                        '<button id="playing" class="button1 bplay" onclick="sendcmd(\'mpc play '
                        + str(i + 1)
                        + "')\"><a>"
                        + str(i + 1)
                        + ". "
                        + pl[i]
                        + "</a></button>"
                    )
                else:
                    rp += (
                        '<button class="button1" onclick="sendcmd(\'mpc play '
                        + str(i + 1)
                        + "')\"><a>"
                        + str(i + 1)
                        + ". "
                        + pl[i]
                        + "</a></button>"
                    )
            self.write(rp)
        elif input == "iplaylist":
            sr = subprocess.check_output("mpc lsplaylists", shell=True).decode("utf-8")
            pl = sr.splitlines(keepends=False)
            pl.sort()
            PLAYlists = pl
            rp = ""
            for i in range(len(pl)):
                rp += (
                    '<button class="button1" onclick="sendcmd(\'mpc load '
                    + pl[i]
                    + "')\"><a>"
                    + str(i + 1)
                    + ". "
                    + pl[i]
                    + "</a></button>"
                )
            self.write(rp)
        elif input == "status":
            status = module_piradionex.get_mpc_status()
            print(json.dumps(module_piradionex.get_mpc_status(), indent=2))
            sr = subprocess.check_output("mpc", shell=True).decode("utf-8")
            self.write(sr)
        elif input == "sttsjson":
            status = module_piradionex.get_mpc_status()
            print(json.dumps(module_piradionex.get_mpc_status(), indent=2))
            self.write(json.dumps(status))
        elif input == "config":
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(CONFIGDATA))
        elif input == "hostname":
            sr = subprocess.check_output("hostname", shell=True).decode("utf-8")
            self.write(sr)
        elif input == "getsleep":
            sst = sleeptimer.update()
            # sst="00:00"
            self.write(sst)
        elif input == "stopsleep":
            sst = sleeptimer.stopcdown()
            self.write("timer stopped")
        elif input == "restart":
            print("This program will restart itself in 2 seconds...")
            interuptDisplay(1, "Restarting app")
            # interuptDisplay(1, "switcing PLAYlists")
            time.sleep(0.5)  # Wait for 5 seconds before restarting
            # Restart the program
            print("Restarting...")
            # self.render("webscr.html", wsurl=urll, tms=_TS)
            rp = "app restarting"
            self.write(rp)
            time.sleep(1.5)
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            self.write("command not recognized")

    def post(self):
        value = self.get_argument("cmd")
        sr = subprocess.check_output("mpc volume " + value, shell=True).decode("utf-8")
        self.write("volume" + sr)
        # print(cmd)


# WebSocket handler
class WSHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        # print("WebSocket opened by ")
        remote_ip = self.request.remote_ip
        try:
            hostname, _, _ = socket.gethostbyaddr(remote_ip)
            print(f"WebSocket opened from {hostname} ({remote_ip})")
            interuptDisplay(1, (f"WebSocket opened from {hostname} [{remote_ip}]"))
        except socket.herror:
            print(f"WebSocket opened from {remote_ip} (hostname not resolved)")
            interuptDisplay(
                1, (f"WebSocket opened from {remote_ip} (hostname not resolved)")
            )
        self.clients.add(self)

    def on_close(self):
        print("WebSocket closed")
        self.clients.remove(self)

    def on_message(self, message):
        sleeptimer.resetas()
        print(f"[WS] Incoming message:{message}"), message
        interuptDisplay(1, (f"[WS] Incoming message:\n{message}"))

        if message.startswith("0>"):
            sbmsg = message[2:]
            # if sbmsg.startswith("mpc"):
            #     stimer.resetas()
            if sbmsg.startswith("mpc load"):
                noReturnSubprocess("mpc clear")
                noReturnSubprocess(sbmsg)
                noReturnSubprocess("mpc play")

                # subprocess.check_output("mpc clear", shell=True)
                # subprocess.check_output(sbmsg, shell=True).decode("utf-8")
                # subprocess.check_output("mpc play   ", shell=True).decode("utf-8")
                global PLAY_CURL
                PLAY_CURL = False
                interuptDisplay(1, "switcing PLAYlists")
            elif sbmsg.startswith("mpc volume"):
                out = subprocess.check_output(
                    sbmsg + " | grep volume | awk '{print$2}'", shell=True
                ).decode("utf-8")
                interuptDisplay(1, "set volume " + out)
            else:
                sr = subprocess.check_output(sbmsg, shell=True).decode("utf-8")
        elif message.startswith("1>"):
            sbmsg = message[2:]
            if sbmsg.startswith("stopsleep"):
                sleeptimer.stopcdown()

    @classmethod
    async def send_message(cls, message):
        for client in cls.clients:
            if client.ws_connection:  # Check if the client is still connected
                await client.write_message(message)


# Tornado application setup
def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/scmd/(\w+)", shellCmd),
            (r"/websocket", WSHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"}),
        ],
        **settings,
    )


async def tick():
    global pulse_
    global secondDigit
    while True:
        pulse_ += 1
        if pulse_ > 15:
            pulse_ = 0
            if secondDigit > 0:
                secondDigit = int(secondDigit / 10)
                os.system("mpc play " + str(secondDigit))
                secondDigit = 0
            # print("tick")
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.name)
        if device.name == "sunxi-ir":
            print("Using device", device.path, "\n")
            # return device
            # print("No device found!")

            app = make_app()
            app.listen(8888)
            mtimer.start()
            try:
                asyncio.ensure_future(print_events(device))
                asyncio.ensure_future(tick())
                # Start the Tornado I/O loop
                print("start tornado")
                tornado.ioloop.IOLoop.current().start()

                # asyncio.run(iorun())
            except KeyboardInterrupt:
                print("try stop")
                mtimer.stop()
                sleep(1)
                print("Keyboard interrupt received, exiting...")
# loop = asyncio.get_event_loop()
# loop.run_forever()


#
# try:
#     event_list = [event.value for event in events]
#     print("Receved command:", event_list)
# except BlockingIOError:
#     print("No commands received. \n")


# dev = InputDevice('/dev/input/event1')
