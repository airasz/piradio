#!usr/bin/env python
# import RPi.GPIO as GPIO
import time
import evdev
from evdev import InputDevice, categorize, ecodes
import os
from time import sleep
import socket
import json
import subprocess
import asyncio
import threading
from evdev import InputDevice

import mpcstimer
import serialdisplay

import tornado
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


#stimer=mpcstimer.mpctimer()
sleeptimer= serialdisplay.sleeptimer()#used as sleep timer

SWITCH_PLAYLIST = False
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0
DBG_EVENT=False
EN_NEXMEDIA_R=False

PLAY_CURL=False

#remot key nexmedia
KR_POWER =  2099200
KR_OPT =    2099287
KR_D_UP =   2099218
KR_D_DOWN = 2099219
KR_VOLUP =  2099202
KR_VOLDOWN = 2099203
KR_STUP =   2099206
KR_STDOWN = 2099207
KR_GREEN=   2099225
KR_OK=      2099221
KR_SLEEP=   2099231
KR_EXIT=    2099216
KR_NUMKEYS=[[1 , 2099228],[2 , 2099229],[3 , 2099230],[4 , 2099264],[5 , 2099265],[6 , 2099266],[7 , 2099268],[8 , 2099269],[9 , 2099270],[10 , 2099271]]
KB_NUMKEYS=[[1 , 458841],[2 , 458842],[3 , 458843],[4 , 458844],[5 , 458845],[6 , 458846],[7 , 458847],[8 , 458848],[9 , 458849],[10 , 458850]]

#KB_NUMKEYS=[[1 , KEY_KP1],[2 , KEY_KP2],[3 , KEY_KP3],[4 , KEY_KP4],[5 , KEY_KP5],[6 , KEY_KP6],[7 , KEY_KP7],[8 , KEY_KP8],[9 , KEY_KP9],[10 , KEY_KP0]]


#temporary flag
TEN = False
NUM_VOL=0
TO_REBOOT= False
HASINTERNET_ = False
MIN_SLEEP=0
MIN_SLEEPV=0
T_LINES=0
TOQ=0
TS_ENABLE=False
STOP_SLEEP=0


def interuptDisplay(delay, msg):
    display.frezeeDisplay(delay)
    display.display(msg, False)

# def interuptDisplay(msg, delay):
#     display.display(msg, False)
#     display.frezeeDisplay(delay)

def load_variable():
    global CDOWN
    global TS_ENABLE
    try:
        with open("timer.json", "r") as f:
            data = json.load(f)
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

def hasInsternet():
    print("check Internet Connection")
    global HASINTERNET_
    try:
        s = socket.create_connection(
              ("www.google.com", 80))
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
display=serialdisplay.display()

def getTotalQ():
    status = "radio volume: 50%"
    os.system("mpc playlist > tmp")
    status = open("tmp", "r").read()
    tq = status.count("\n") + 1
    global SWITCH_PLAYLIST

    if "muslim" in status:
        print("playlist muslim detected")
        SWITCH_PLAYLIST = False
    # if tq < 10:
    #     SWITCH_PLAYLIST = True
    print("total queue = " + str(tq))
    return tq

# os.system("mpc volume 50")
os.system("ir-keytable -p nec")
#os.system("/usr/bin/mpc play")
TOQ = getTotalQ()

# os.system("/usr/bin/python3 mpcsleeper.py")
def getVol():
    status = subprocess.check_output("mpc volume | grep volume | awk '{print$2}'",shell=True).decode("utf-8").replace("%","")
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
    status = "radio volume: 50%"
    os.system("mpc > tmp")
    status = open("tmp", "r").read()
    # volpos = status.index('playing')
    if "playing" in status:
        return True
    else:
        return False

def playToggle():
    os.system("mpc "+ ("stop" if getPlayState() else "play"))
    # if (getPlayState()) is True:
    #     os.system("mpc stop")
    # else:
    #     os.system("mpc play")

def setVOL(up):
    status = ""
    vol=""
    status = subprocess.check_output(("mpc volume +5 | grep volume | awk '{print$2}'") if up else ("mpc volume -5 | grep volume | awk '{print$2}'"), shell=True).decode("utf-8")
    print("vol "+status)
    interuptDisplay(3, "set volume\n"+ status)
#     if (getPlayState()) is True:
#         status = subprocess.check_output("mpc volume | awk '{print$2}'", shell=True)
#         vol=str(status.decode("utf-8"))
#         vol=vol[:len(vol)-2]
#         intvol = int(vol)
#         os.system("mpc "+ ("volume +5" if up else "volume -5"))
#
#         interuptDisplay(3, "set volume\n"+ vol)

        # if up is True:
        #     os.system("mpc volume +5")
        #     intvol+=5
        #     display.display("v "+ vol)
        #
        # else:
        #     os.system("mpc volume -5")
        #     intvol-=5
        #     display.display("v "+ vol)
        #

def setSTATION(next):
    if (getPlayState()) is True:
        interuptDisplay(3, "playing next" if next else "playing previous")
        os.system("mpc "+ ("next" if next else "prev"))

def reboot():
    global TO_REBOOT
    if TO_REBOOT is False:
        TO_REBOOT = True
        interuptDisplay(8, "press again to reboot")

    else:
        interuptDisplay(5, "rebooting...")
        sleep(1)
        os.system("reboot")

VOLTO=0
def playPos(pos):
    global TEN
    global VOLTO
    global NUM_VOL
    global MIN_SLEEP
    global MIN_SLEEPV
    status = ""
    if TEN is True:
        # display.display("playing pos "+ str(pos + 10 if TEN else pos))
        global TOQ
        if TOQ > 10:
            pos = pos + 10
            interuptDisplay(3, "play pos "+ str(pos))
            os.system("mpc play " + str(pos))
            TEN = False
        else:
            interuptDisplay(3, "play pos "+ str(pos))
            os.system("mpc play " + str(pos))

    else:
        # display.display("volume to "+ str(pos + 10 if TEN else pos))
        if NUM_VOL==0 and MIN_SLEEP==0:
            interuptDisplay(3, "play pos "+ str(pos))
            os.system("mpc play " + str(pos))
            exitset()
            return
        if NUM_VOL == 1:
            VOLTO=pos * 10
            interuptDisplay(5, "volume to "+ str(pos)+"x")
            print("start vol========== "+ str(VOLTO))
            NUM_VOL =2
        elif NUM_VOL == 2:
            VOLTO+= pos
            NUM_VOL=0
            interuptDisplay(5, "volume to "+ str(VOLTO))
            os.system("mpc volume " + str(VOLTO))
            exitset()

        if MIN_SLEEP==1:
            # MIN_SLEEPV+=pos**MIN_SLEEP
            MIN_SLEEPV=0
            MIN_SLEEPV=pos*10
            interuptDisplay(5, "sleep in "+ str(pos)+"x minutes")
            #
            MIN_SLEEP=2
        elif MIN_SLEEP==2:
            MIN_SLEEPV+=pos
            interuptDisplay(5, "sleep in "+ str(MIN_SLEEPV)+" minutes\nClick OK to confirm")



def startVol():
    global NUM_VOL
    global TEN
    if TEN is True:
        TEN =False
    NUM_VOL=1
    interuptDisplay(8, "jump volume to...")
    display.onmenu(True)


def startTenPos():
    global TEN
    global NUM_VOL
    TEN = True
    if NUM_VOL !=0:
        NUM_VOL=0
    interuptDisplay(8, "set play pos 1...")
    display.onmenu(True)

def startsetsleep():
    global stimerStop
    global NUM_VOL
    global TEN
    global MIN_SLEEP
    global STOP_SLEEP
    load_variable()
    display.onmenu(True)
    if TS_ENABLE is True:
        if STOP_SLEEP==0:
            STOP_SLEEP+=1
            interuptDisplay(5, "press again to stop")
        else:
            jdata={"enable":False,
                "startrun":False,
                "svalue":0,
                "seconds":0
            }
            with open("timer.json", "w") as f:
                json.dump(jdata, f)
            interuptDisplay(5, "sleep timer stopped")

            STOP_SLEEP=0
    else:
        interuptDisplay(8, "set sleep...")
        MIN_SLEEP=1

    # if stimer.isrunning() is True:
    #     if stimerStop==0:
    #         interuptDisplay(5, "timer is running\npress again to stop")
    #         display.resettimer()
    #         stimerStop+=1
    #     elif stimerStop==1:
    #         interuptDisplay(5, "timer is stopped")
    #         stimerStop=0
    #         display.resettimer()
    # else:
    #     interuptDisplay(5, "set sleep...")
    #     MIN_SLEEP=1
    #     display.resettimer()

def ok():
    global MIN_SLEEP
    global MIN_SLEEPV
    if MIN_SLEEP>0:
        # stimer.startcdown(MIN_SLEEPV)
        # os.system("/usr/bin/python3 startsleeper.py "+ str(MIN_SLEEPV))
        interuptDisplay(5, "sleep timer starting for "+str(MIN_SLEEPV) +" minutes")
        MIN_SLEEP=0
        sleeptimer.startcdown(MIN_SLEEPV)
        exitset()

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
    display.onmenu(False)


def getstationlen(): #get total playlist
    global T_LINES
    global TOQ
    global SWITCH_PLAYLIST
    status = subprocess.check_output("mpc playlist", shell=True)
    status =  status.decode("utf-8")
    if "muslim" in status:
        SWITCH_PLAYLIST = False
    T_LINES = status.count('\n')
    TOQ = T_LINES
    print("playlist="+ str(T_LINES))
    # print(T_LINES)

def switchPLAYLIST():
    global SWITCH_PLAYLIST
    # global PLAYlists
    # SWITCH_PLAYLIST = not SWITCH_PLAYLIST
    getstationlen()
    if SWITCH_PLAYLIST is True:
        SWITCH_PLAYLIST=False
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
    print(("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else ("mpc load " + PLAYlists[0]))
    status = cmd("mpc load " + PLAYlists[1]) if SWITCH_PLAYLIST else cmd("mpc load " + PLAYlists[0])
    getstationlen()

    interuptDisplay(2, status)
    sleep(1)
    status = cmd("mpc play")
    display.frezeeDisplay(1)

def processIR(irval):
    global EN_NEXMEDIA_R
    # print(irval)
    # display.resettimer()
    #hexval = hex(irval)
   # print(hexval)
    # sval=str(irval)
    #
    # display.resettimer(sval)
    # interuptDisplay(sval)
    if irval== KR_GREEN:
        EN_NEXMEDIA_R= not EN_NEXMEDIA_R
        interuptDisplay(3, "REMOTE control\n"+("unlocked" if EN_NEXMEDIA_R else "locked"))
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
            os.system("mpc play")
        elif irval == 2099277:
            print("stop")
            interuptDisplay(3, "player stopped")
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
        elif irval==KR_SLEEP:
            # msleep(20)
            startsetsleep()
        elif irval==KR_OK:
            ok()
        elif irval==KR_EXIT:
            exitset()
    else:
        if irval >2000000:
            interuptDisplay(5, "unregistered key remote\nor this remote locked")

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
        os.system("mpc play")
        # status = cmd("mpc play")
        getPlayState()
    if ecode == STOP:
        interuptDisplay(3, "player stopped")
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
SCOUNT=0
def infinity():
    global SCOUNT
    SCOUNT +=1
    if SCOUNT == 10:
        if display.getmenu() is True:
            display.onmenu(False)
        SCOUNT=0

    threading.Timer(1, infinity).start()

infinity()

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
            print(categorize(event))
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
        if event.value > 2000000:
            sleeptimer.resetas()
        if DBG_EVENT is True:
            print("===============end debug==========")
        #print(event.code)
#for device in ir, keybd:
    #asyncio.ensure_future(print_events(device))




#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"), static_path = os.path.join(os.path.dirname(__file__), "static")
    )


def broadcast_message(message):
    print("broadcast_message "+ message)
    for client in WSHandler.clients:
        client.write_message(message)
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
        if curlval!="":
            # stimer.resetas()
            global PLAY_CURL
            if PLAY_CURL is False:
                status = cmd("mpc clear")
            sleep(0.1)
            status = cmd("mpc add " + curlval)
            # display.frezeeDisplay(2)
            # myoled.displayfs(status, 16)
            sleep(1)
            status = cmd("mpc play")
            # displaytooled(status)
            broadcast_message("info="+status)
            # display.frezeeDisplay(3)
            PLAY_CURL=True
            # pass
        # ok()
        self.render("index.html")

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
        elif input== "hostname":
            sr=subprocess.check_output("hostname", shell=True).decode("utf-8")
            self.write(sr)
        elif input== "getsleep":
            sst=sleeptimer.update()
            # sst="00:00"
            self.write(sst)
        elif input== "stopsleep":
            sst=sleeptimer.stopcdown()
            self.write("timer stopped")
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
        print(f"Client connected: {self.request.remote_ip}")
        self.clients.add(self)

    def on_close(self):
        print("WebSocket closed")
        self.clients.remove(self)

    def on_message(self, message):
        sleeptimer.resetas()
        print (f'[WS] Incoming message:{message}'), message

        if message.startswith("0>"):
            sbmsg=message[2:]
            # if sbmsg.startswith("mpc"):
            #     stimer.resetas()
            if sbmsg.startswith("mpc load"):
                subprocess.check_output("mpc clear", shell=True)
                subprocess.check_output(sbmsg, shell=True).decode("utf-8")
                subprocess.check_output("mpc play   ", shell=True).decode("utf-8")
                global PLAY_CURL
                PLAY_CURL=False
            else:
                sr=subprocess.check_output(sbmsg, shell=True).decode("utf-8")
        elif message.startswith("1>"):
            sbmsg=message[2:]
            if sbmsg.startswith("stopsleep"):
                sleeptimer.stopcdown()
    @classmethod
    async def send_message(cls, message):
        for client in cls.clients:
            if client.ws_connection:  # Check if the client is still connected
                await client.write_message(message)


# Tornado application setup
def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/scmd/(\w+)', shellCmd),
        (r"/websocket", WSHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"})
    ],
        **settings)




devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.name)
    if device.name == "sunxi-ir":
        print("Using device", device.path, "\n")
        #return device
    # print("No device found!")
    asyncio.ensure_future(print_events(device))


    app = make_app()
    app.listen(8888)

    # Start the Tornado I/O loop
    tornado.ioloop.IOLoop.current().start()

loop = asyncio.get_event_loop()
loop.run_forever()




#
# try:
#     event_list = [event.value for event in events]
#     print("Receved command:", event_list)
# except BlockingIOError:
#     print("No commands received. \n")


# dev = InputDevice('/dev/input/event1')


