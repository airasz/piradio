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

import re
import math
import psutil


# import oledis
# import module_radio
# import mpcstimer

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT

from pathlib import Path
from PIL import ImageFont

import tornado
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

# import wsradio


# ----------------OLED DISPLAY SETUP------------
font_path = str(Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf"))
font2 = ImageFont.truetype(font_path, 10)
font3 = ImageFont.truetype(font_path, 30)


def do_nothing(obj):
    pass


serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=2)
device.cleanup = do_nothing

# Add a global variable to store the serial transport
serial_transport = None

# Global variable dictionary
G_VAR = {
    "EN_NEXMEDIA_R": False,
    "SWITCH_PLAYLIST": True,
    "P_VOL": 0,
    "PLAY_CURL": False,
    "PLAYLIST_POINTER": 0,
    "PICK_PLAYLIST": False,
    "GOTOSTATION": False,
    "PULSE_COUNT": 0,
    "SECOND_DIGIT": 0,
    "SCOUNT": 0,
    "PREV_STATUS": "",
    "PREV_PLAYLIST": "",
    "TORESTART": False,
    "VOLTO": 0,
    "LOCAL_IP": "192.168.1.123",
    "CPU_TEMP": "",
    "NETSTAT": "0MB",
    "SYSTEM_READY": 0,
    "T_ENABLE": False,
    "SEC_CD": 0,
    "AUTOSTOP_COUNT_DOWN": True,
    "AUTOSTOP_SECOND_CDOWN": 0,
    "ASSECMX": 3600,
    "PLAYING": True,
    "DISPLAY_PAGER": 0,
    "U_COUNT": 20,
    "MAXUCOUNT": 25,
    "STOP_COUNT": 0,
    "SCREEN_SLEEP": False,
    "NUM_VOL": 0,
    "MINUTE_SLEEP": 0,
    "MIN_SLEEP_VALUE": 0,
    "TO_REBOOT": False,
    "TO_RESTARTAPP": False,
    "TS_ENABLE": False,
    "STOP_SLEEP": 0,
    "CDOWN": 0,
    "NEXT_PLAYLIST": False,
}
CONFIGDATA = {}
RADIO_STATUS = {}
PLAYlists = []
# Remote control key codes as JSON data
REMOTE_CODES = {}


config_path = "radioconfig.json"
remote_path = "remote_code.json"


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

KR_nNUM = [
    [1, "41038C7"],
    [2, "410B847"],
    [3, "4107887"],
    [4, "41002FD"],
    [5, "410827D"],
    [6, "41042BD"],
    [7, "41022DD"],
    [8, "410A25D"],
    [9, "410629D"],
    [10, "410E21D"],
]

KR_cNUM = [
    [1, "FF30CF"],
    [2, "FFB04F"],
    [3, "FF708F"],
    [4, "FF08F7"],
    [5, "FF8877"],
    [6, "FF48B7"],
    [7, "FF28D7"],
    [8, "FF04FB"],
    [9, "FF847B"],
    [10, "FF44BB"],
]

KR_wNUM = [
    [1, "FD40BF"],
    [2, "FDC03F"],
    [3, "FD20DF"],
    [4, "FDA05F"],
    [5, "FD609F"],
    [6, "FDE01F"],
    [7, "FD10EF"],
    [8, "FD906F"],
    [9, "FD50AF"],
    [10, "FD30CF"],
]

KR_eNUM = [
    [1, "FD4AB5"],
    [2, "FD0AF5"],
    [3, "FD08F7"],
    [4, "FD6A95"],
    [5, "FD2AD5"],
    [6, "FD28D7"],
    [7, "FD728D"],
    [8, "FD32CD"],
    [9, "FD30CF"],
    [10, "FDF00F"],
]
# temporary flag


class oled:
    def display(self, msg):
        with canvas(device) as draw:
            draw.text((0, 0), msg, fill="white", font=font2)
        return

    def display(self, msg, cursor):
        with canvas(device) as draw:
            draw.text(cursor, msg, fill="white", font=font2)
        return

    def display_onpos(self, msg, randompos):
        mx = 128 - len(msg) * 6
        # print("mx="+str(mx))
        if mx < 0:
            mx = 0
        ypos = random.randint(0, 54) if randompos else 0
        xpos = random.randint(0, mx) if randompos else 0
        with canvas(device) as draw:
            draw.text((xpos, ypos), msg, fill="white", font=font2)
        return

    def displaybig(self, msg):
        with canvas(device) as draw:
            draw.text((0, 0), msg, fill="white", font=font3)
        return

    def displayfs(self, msg, font_size):
        cfont = ImageFont.truetype(font_path, font_size)
        with canvas(device) as draw:
            draw.text((0, 0), msg, fill="white", font=cfont)
        return

    def displayfscs(self, msg, font_size, cursor):
        cfont = ImageFont.truetype(font_path, font_size)
        with canvas(device) as draw:
            draw.text(cursor, msg, fill="white", font=cfont)
        return

    def showmsg(self, msg):
        show_message(device, msg, fill="white", font=font2)
        return

    def clear(self, cmode):
        if cmode == 0:
            device.clear()  # clears to display immediately
        elif cmode == 1:
            device.hide()  # put the device into low-power sleep, switching the screen off
        # device.show() # wake the device from low-power sleep, which restores the previously displayed value
        return

    def show(self):
        device.show()  # wake the device from low-power sleep, which restores the previously displayed value
        return


myoled = oled()


def loop():

    old_status = ""
    status = ""
    status = subprocess.check_output("mpc", shell=True).decode("utf-8")
    if "playing" in status or "paused" in status:
        G_VAR["PLAYING"] = True
    else:
        G_VAR["PLAYING"] = False
    if G_VAR["U_COUNT"] == 20:
        if "playing" in status or "paused" in status:
            # displaytooled2()
            displayto_oled(status)
            # stimer.updateplayer(True)
            G_VAR["MAXUCOUNT"] = 25
            G_VAR["STOP_COUNT"] = 0
        else:
            G_VAR["MAXUCOUNT"] = 20
            G_VAR["STOP_COUNT"] += 1
            # print("G_VAR["STOP_COUNT"]" + str(G_VAR["STOP_COUNT"]))
            if G_VAR["STOP_COUNT"] > 600:
                myoled.display("", (0, 0))
                G_VAR["STOP_COUNT"] = 201
                if G_VAR["SCREEN_SLEEP"] is False:
                    G_VAR["SCREEN_SLEEP"] = True
                    # myoled.clear(1)
            else:
                if G_VAR["STOP_COUNT"] == 2:
                    G_VAR["LOCAL_IP"] = G_VAR["LOCAL_IP"].replace("IP: ", "")
                secac = sleeptimer.getsecac()
                if secac == str(G_VAR["ASSECMX"] + 1):
                    myoled.display(
                        "player stopped due\n1 hour no user\nactivity", (0, 0)
                    )
                    os.system()
                else:
                    ypos = random.randint(0, 30)
                    xpos = random.randint(0, 50)
                    myoled.display("player stopped\n" + G_VAR["LOCAL_IP"], (xpos, ypos))
            # sleep(0.4)
    G_VAR["U_COUNT"] += 1
    if G_VAR["U_COUNT"] == 25:

        G_VAR["SYSTEM_READY"] += 1
        if G_VAR["SYSTEM_READY"] > 8:
            G_VAR["SYSTEM_READY"] = 8
        getNetData()
        updateCPUtemp()
        # NETSTAT =  status.decode("utf-8")
    if G_VAR["U_COUNT"] > G_VAR["MAXUCOUNT"]:
        G_VAR["U_COUNT"] = 20

    old_status = status


# split and paged all information to display
def displayto_oled(status):
    get_mpc_status()
    print(json.dumps(get_mpc_status(), indent=2))
    if len(G_VAR["LOCAL_IP"]) < 8:
        getlocal_ip()

    mlpl = 22  # maximum length per line
    # srink status
    if "repeat" in status:
        inrep = status.index("repeat")
        status = status[:inrep]

        # crop station info
        inbrace = status.index("[")
        station = status[:inbrace]
        # print("station = " + station)
        # split limited length char to list
        infolist = textwrap.wrap(station, mlpl)

        # crop playing info
        indvol = status.index("volume")
        indel = status.index("(") - 1
        state = status[inbrace:indel]
        state = state.replace("#", " ")
        if "0:00" in state:
            state = state.replace("[", "")
            state = state.replace("]", "")
            state = state.replace("/0:00", "")
        # split limited length char to list
        msglist = textwrap.wrap(state, mlpl)

        # crop volume info
        stvol = status[indvol:]

        # print("state = " + state)

        for i in infolist:
            msglist.append(i)

            # msglist.append(i)
        msglist.append(stvol)

    # load_variable()
    if G_VAR["T_ENABLE"] is True:
        # if stimer.isrunning() is True:
        mins, secs = divmod(G_VAR["SECOND_CDOWN"], 60)
        hours, mins = divmod(mins, 60)
        timer = f"{hours:02d}:{mins:02d}:{secs:02d}"
        sst = "sleep in : " + timer
        # sst="sleep in : "+stimer.update()
        msglist.append(sst)
    msglist.append(G_VAR["LOCAL_IP"])
    # msglist.append("test")
    msglist.append(G_VAR["NETSTAT"])
    msglist.append(G_VAR["CPU_TEMP"])

    status = status.replace("(0%)", "")
    status = status.replace("(volume", "\nvolume")

    # myoled.display(status, (0,0))

    # myoled.showmsg(status)

    msglist.append(sysinfo())
    totline = len(msglist)
    # print(totline)
    sm = ""
    text = ""
    totpage = int(len(msglist) / 4)
    ttlline = 4 * totpage
    if totline > ttlline:
        totpage += 1  # get actual page

    for x in range(4):
        idx = (G_VAR["DISPLAY_PAGER"] * 4) + x
        if idx < totline:
            sm = str(msglist[idx])
            text += sm
            text += "\n"
        else:
            break

        # print(text)
    myoled.display(text, (0, 0))
    text = ""
    G_VAR["DISPLAY_PAGER"] += 1
    if G_VAR["DISPLAY_PAGER"] > (totpage - 1):
        G_VAR["DISPLAY_PAGER"] = 0


class sleeptimer:
    def startcdown(self, minutes):
        G_VAR["T_ENABLE"] = True
        G_VAR["SECOND_CDOWN"] = minutes * 60
        return

    # cancel sleep timer
    def stopcdown(self):
        G_VAR["T_ENABLE"] = False
        G_VAR["SECOND_CDOWN"] = 0
        print("sleep timer stopped by user")
        return

    def countdown(self):
        # print("sec cd = "+str(SEC_CD))
        if G_VAR["T_ENABLE"] is True and G_VAR["PLAYING"] is True:
            mins, secs = divmod(G_VAR["SECOND_CDOWN"], 60)
            timer = f"{mins:02d}:{secs:02d}"
            # print(f'Time left: {timer}', end='\r')
            G_VAR["SECOND_CDOWN"] -= 1
            # print("iradio_oled" +str(SEC_CD))
            if G_VAR["SECOND_CDOWN"] == 0:
                print("\nTime's up!")
                os.system("mpc stop")
                send_wall_message("mpc stopped due sleep timer defined by user")
                G_VAR["T_ENABLE"] = False
                # quit()

    # auto stop reset counting
    def resetAutoStop(self):
        # print("auto stop timer resetted")
        G_VAR["AUTOSTOP_SECOND_CDOWN"] = 0

    # get auto stop second running
    def getsecac(self):
        return str(G_VAR["AUTOSTOP_SECOND_CDOWN"])

    def autostop(self):
        if G_VAR["AUTOSTOP_COUNT_DOWN"] is True and G_VAR["PLAYING"] is True:
            G_VAR["AUTOSTOP_SECOND_CDOWN"] += 1
            # print("iradio_oled auto stop  "+str(G_VAR["AUTOSTOP_SECOND_CDOWN"]))
            if G_VAR["AUTOSTOP_SECOND_CDOWN"] == G_VAR["ASSECMX"]:
                print("\nauto stop due a 1 hour no user activity!")
                send_wall_message("mpc stopped due 1 hour without user control")
                os.system("mpc stop")
            elif G_VAR["AUTOSTOP_SECOND_CDOWN"] > (G_VAR["ASSECMX"] + 1):
                G_VAR["AUTOSTOP_SECOND_CDOWN"] = G_VAR["ASSECMX"] + 1

    def beat(self):
        self.countdown()
        self.autostop()

    def isrunning(self):
        return G_VAR["T_ENABLE"]

    def update(self):
        # print("sec cd = "+str(SEC_CD))
        if G_VAR["T_ENABLE"] is True:
            RADIO_STATUS["sleeptimer"]["second_countdown"] = seconds_to_time(G_VAR["SECOND_CDOWN"])
            print(f' sleep countdown json= {RADIO_STATUS["sleeptimer"]["countdown"]}')
            mins, secs = divmod(G_VAR["SECOND_CDOWN"], 60)
            hours, mins = divmod(mins, 60)
            timer = f"{hours:02d}:{mins:02d}:{secs:02d}"
            return "sleep in > " + str(timer)
        else:
            return "off"  # do not change


sleeptimer = sleeptimer()


class display:
    def resettimer(self):
        G_VAR["U_COUNT"] = 15
        print("reset timer")
        return

    def setPage(self, up):
        G_VAR["U_COUNT"] = 19
        print(f'G_VAR["U_COUNT"] = {G_VAR["U_COUNT"]}')
        if up is True:
            G_VAR["DISPLAY_PAGER"] += 1
        else:
            G_VAR["DISPLAY_PAGER"] = 0
        displayto_oled(status)

    def delay(self, time):
        if time > 0:
            G_VAR["U_COUNT"] = 0 - time
        return

    def frezeeDisplay(self, delay):
        G_VAR["U_COUNT"] = 20 - delay
        # print("reset timer for " + str(delay))
        return

    def display(self, msg, pos):
        myoled.display(msg, pos)
        return

    def displaybig(self, msg):
        myoled.displaybig(msg)
        return

    def displayfs(self, msg, fs):
        myoled.displayfs(msg, fs)
        G_VAR["DISPLAY_PAGER"] = 0
        return

    def display(self, msg, rndom):
        mx = 128 - len(msg) * 6
        print("mx=" + str(mx))
        if mx < 0:
            mx = 0
        ypos = random.randint(0, 54) if rndom else 0
        xpos = random.randint(0, mx) if rndom else 0
        myoled.display(msg, (xpos, ypos))
        return


display = display()


def to_bool(value: str) -> bool:
    return value.lower() == "on"


def time_to_seconds(t: str) -> int:
    """Convert mm:ss string to total seconds"""
    try:
        m, s = t.split(":")
        return int(m) * 60 + int(s)
    except Exception:
        return 0


def seconds_to_time(sec: int) -> str:
    """Convert seconds to mm:ss format"""
    if sec < 0:
        sec = 0
    m, s = divmod(sec, 60)
    return f"{m}:{s:02d}"


def get_mpc_status():
    result = subprocess.run(["mpc", "status"], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()

    if not lines:
        return {"error": "mpc returned no output (MPD might not be running)"}

    global RADIO_STATUS

    # --- Case: stopped ---
    if len(lines) == 1 and ("volume:" in lines[0] or "stopped" in lines[0].lower()):
        RADIO_STATUS.update(
            {
                "artist": None,
                "title": None,
                "mode": "stopped",
                "is_playing": False,
                "is_paused": False,
                "is_stopped": True,
                "position": {"current": 0, "total": 0},
                "time": {
                    "elapsed": "0:00",
                    "total": "0:00",
                    "elapsed_seconds": 0,
                    "total_seconds": 0,
                    "remaining_seconds": 0,
                    "remaining_time": "0:00",
                },
                "progress_percent": 0,
                "progress_ratio": 0.0,
                "duration_ratio": 0.0,
                "volume": None,
                "repeat": False,
                "random": False,
                "single": False,
                "consume": False
            }
        )
        return RADIO_STATUS

    # --- Case: playing or paused ---
    if " - " in lines[0]:
        artist, title = lines[0].split(" - ", 1)
        RADIO_STATUS["artist"] = artist
        RADIO_STATUS["title"] = title
    else:
        RADIO_STATUS["artist"] = None
        RADIO_STATUS["title"] = lines[0]

    # line 2: mode, position, time, progress
    mode_match = re.search(r"\[([^\]]+)\]", lines[1])
    mode = mode_match.group(1).lower() if mode_match else "unknown"
    RADIO_STATUS["mode"] = mode
    RADIO_STATUS["is_playing"] = mode == "playing"
    RADIO_STATUS["is_paused"] = mode == "paused"
    RADIO_STATUS["is_stopped"] = mode == "stopped"

    pos_match = re.search(r"#(\d+)/(\d+)", lines[1])
    pos_cur, pos_total = pos_match.groups() if pos_match else ("0", "0")
    pos_cur, pos_total = int(pos_cur), int(pos_total)

    time_match = re.search(r"(\d+:\d+)/(\d+:\d+)", lines[1])
    elapsed, total = time_match.groups() if time_match else ("0:00", "0:00")

    progress_match = re.search(r"\((\d+)%\)", lines[1])
    progress = int(progress_match.group(1)) if progress_match else 0

    elapsed_sec = time_to_seconds(elapsed)
    total_sec = time_to_seconds(total)
    remaining_sec = total_sec - elapsed_sec
    remaining_time = seconds_to_time(remaining_sec)

    progress_ratio = (elapsed_sec / total_sec) if total_sec > 0 else 0.0
    duration_ratio = (pos_cur / pos_total) if pos_total > 0 else 0.0

    RADIO_STATUS["position"] = {"current": pos_cur, "total": pos_total}
    RADIO_STATUS["time"] = {
        "elapsed": elapsed,
        "total": total,
        "elapsed_seconds": elapsed_sec,
        "total_seconds": total_sec,
        "remaining_seconds": remaining_sec,
        "remaining_time": remaining_time,
    }
    RADIO_STATUS["progress_percent"] = progress
    RADIO_STATUS["progress_ratio"] = round(progress_ratio, 3)
    RADIO_STATUS["duration_ratio"] = round(duration_ratio, 3)

    # line 3: volume + flags
    if len(lines) >= 3:
        volume_match = re.search(r"volume:\s*(\d+)%", lines[2])
        RADIO_STATUS["volume"] = int(volume_match.group(1)) if volume_match else None

        def extract_flag(name):
            m = re.search(rf"{name}:\s*(\w+)", lines[2])
            return to_bool(m.group(1)) if m else False

        RADIO_STATUS["repeat"] = extract_flag("repeat")
        RADIO_STATUS["random"] = extract_flag("random")
        RADIO_STATUS["single"] = extract_flag("single")
        RADIO_STATUS["consume"] = extract_flag("consume")
    else:
        RADIO_STATUS.update(
            {
                "volume": None,
                "repeat": False,
                "random": False,
                "single": False,
                "consume": False,
            }
        )
    RADIO_STATUS.update(
        {
            "sleeptimer": {
                "enable": False,
                "second_countdown": 120,
                "countdown": "0:00",
                "auto_stop": {
                    "enable": False,
                    "second_countdown": 3600,
                    "second_max": 3600,
                    "countdown": "0:00",
                },
            }
        }
    )
    return RADIO_STATUS


def load_variable():
    try:
        with open("/home/timer.json", "r") as f:
            data = json.load(f)
            G_VAR["T_ENABLE"] = data.get("enable", False)
            G_VAR["SECOND_CDOWN"] = data.get("seconds", 120)
    except FileNotFoundError:
        pass


def load_remote_codes():
    print("load remote data")
    global REMOTE_CODES
    try:
        with open(remote_path, "r") as f:
            REMOTE_CODES = json.load(f)

    except FileNotFoundError:
        pass


load_remote_codes()


# print(REMOTE_CODES)
def getlocal_ip():
    cmd = "hostname -I | awk '{print$1}'"
    result = subprocess.check_output(cmd, shell=True)
    G_VAR["LOCAL_IP"] = result.decode("utf-8")
    if ":" in G_VAR["LOCAL_IP"]:
        G_VAR["LOCAL_IP"] = G_VAR["LOCAL_IP"][: (G_VAR["LOCAL_IP"].index(":") - 4)]
    G_VAR["LOCAL_IP"] = G_VAR["LOCAL_IP"].replace("\n", "")
    G_VAR["LOCAL_IP"] = "IP: " + G_VAR["LOCAL_IP"]
    print(G_VAR["LOCAL_IP"])


getlocal_ip()


def updateCPUtemp():
    cmd = "cat /sys/class/thermal/thermal_zone0/temp"
    result = subprocess.check_output(cmd, shell=True)
    G_VAR["CPU_TEMP"] = "cpu temp: " + result.decode("utf-8")[:2] + "c"
    # print(cputemp)


def sysinfo():
    sinfo = ""
    cpu_percent = psutil.cpu_percent(interval=1)
    sinfo = f"CPU: {cpu_percent}% "
    memory_usage = psutil.virtual_memory()
    sinfo += f"Mem: {memory_usage.percent}%"
    return sinfo


def getNetData():
    # required intall netstat
    OUT = subprocess.check_output(
        "netstat -e -n -i | grep wlan0  -A 10 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'",
        shell=True,
    )
    # OUT = subprocess.check_output("ifconfig wlan0 | grep wlan0  -A 10 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'", shell=True)
    G_VAR["NETSTAT"] = str(OUT)
    sbr = G_VAR["NETSTAT"].index("(") + 1
    ebr = G_VAR["NETSTAT"].index(")")
    G_VAR["NETSTAT"] = "RX = " + G_VAR["NETSTAT"][sbr:ebr]
    G_VAR["NETSTAT"] = G_VAR["NETSTAT"].replace("i", "")

    dbm = subprocess.check_output(
        "/usr/sbin/iwconfig wlan0 | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2",
        shell=True,
    )
    signal = dbm.decode("utf-8")
    G_VAR["NETSTAT"] = G_VAR["NETSTAT"] + dbtopercent(dbm)  # + signal[1:]


def dbtopercent(value):
    inval = int(value)
    if inval != 0:
        percent = 100 * (1 - ((-1) - inval) / ((-1) - (-98)))
        pct = str(math.floor(percent))
        return " sig: " + pct + "%"
    else:
        return " sig: 0%"


def send_wall_message(message: str):
    try:
        # Send the message using the 'wall' command
        subprocess.run(["wall"], input=message.encode(), check=True)
        print("Message sent to all logged-in users.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send message: {e}")


def interuptDisplay(delay, fontsize, msg):
    G_VAR["U_COUNT"] = 20 - delay
    if fontsize == 0:
        myoled.display_onpos(msg, False)
    else:
        G_VAR["DISPLAY_PAGER"] = 0
        myoled.displayfs(msg, fontsize)


def load_variable():
    try:
        with open("/home/timer.json", "r") as f:
            data = json.load(f)
            G_VAR["CDOWN"] = data.get("seconds", G_VAR["CDOWN"])
            G_VAR["TS_ENABLE"] = data.get("enable", False)
    except FileNotFoundError:
        pass


def load_config():
    global CONFIGDATA
    try:
        with open(config_path, "r") as f:
            CONFIGDATA = json.load(f)
            REMOTES = CONFIGDATA.get("remote", "")
            G_VAR["TS_ENABLE"] = CONFIGDATA.get("timer", {}).get("enable", False)
            G_VAR["SECOND_CDOWN"] = CONFIGDATA.get("timer", {}).get("seconds", 120)
            if CONFIGDATA.get("autoload", "true") is True:
                os.system("mpc play")
                print("auto play by config")
    except FileNotFoundError:
        pass


load_config()


def save_config():
    global CONFIGDATA
    with open(config_path, "w") as f:
        json.dump(CONFIGDATA, f, indent=4)


# print(f'configdata= {CONFIGDATA}')
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


PLAYlists = cmd("mpc lsplaylists").splitlines(keepends=False)
PLAYlists = sorted(PLAYlists, key=str.lower)


def getVol():
    status = "radio volume: 50%"
    status = cmd("mpc")
    displaytooled(status)
    # status= mpc("mpc status | grep -o 'volume: [0-9]\+' | sed 's/volume: //'")
    G_VAR["P_VOL"] = int(
        cmd("mpc status | grep -o 'volume: [0-9]\+' | sed 's/volume: //'")
    )


def mute():
    getVol()
    print("P_VOL=" + str(G_VAR["P_VOL"]))
    if G_VAR["P_VOL"] > 0:
        G_VAR["CURENT_VOL"] = G_VAR["P_VOL"]
        # os.system("mpc volume 0")
        status = cmd("mpc volume 0")
    else:
        status = cmd("mpc volume " + str(G_VAR["CURENT_VOL"]))


def getPlayState():
    status = ""
    status = cmd("mpc")

    if "playing" in status:
        return True
    elif "paused" in status:
        return True
    else:
        return False


def startVol():
    interuptDisplay(8, 15, "jump volume...")
    exitset(False)
    G_VAR["NUM_VOL"] = 1


stimerStop = 0


def startsetsleep():
    exitset(False)
    global stimerStop
    G_VAR["MINUTE_SLEEP"] = 1

    # load_variable()
    if sleeptimer.isrunning() is True:
        if stimerStop == 0:
            interuptDisplay(3, 0, "timer is running\npress again to stop")
            stimerStop += 1
        elif stimerStop == 1:
            display.frezeeDisplay(3)
            sleeptimer.stopcdown()
            interuptDisplay(3, 0, "timer is stopped")
            stimerStop = 0
    else:
        interuptDisplay(8, 0, "set sleep...")
        G_VAR["MINUTE_SLEEP"] = 1


def startTenPos():
    interuptDisplay(8, 0, "jump station to\n10 + ...")
    exitset(False)
    G_VAR["TEN_PLUS"] = True


def startPlistTo():
    exitset(False)
    G_VAR["PICK_PLAYLIST"] = True
    pls = ""
    ids = 0
    dbl = 0
    PLAYlists.sort()
    for item in PLAYlists:
        dbl += 1
        nl = "\n"
        pls += f'{str(ids+1)}. {str(item)}{nl if dbl%2==0 else "  "}'
        ids += 1
    interuptDisplay(8, 0, f"select.\n{pls}")


def seekthrough(forward):
    status = ""
    vol = ""
    status = cmd("mpc seekthrough " + ("+1:00" if forward else "-1:00"))
    print("vol " + status)


def setSTATION(next):
    status = ""
    ypos = random.randint(0, 54)
    xpos = random.randint(0, 50)
    display.frezeeDisplay(3)
    if (getPlayState()) is True:
        interuptDisplay(2, 18, "playing\nnext" if next else "playing\nprevious")
        noReturnSubprocess(f'mpc {("next" if next else "prev")}')
    print("status = " + status)
    broadcast_message("resettimer")


def getCurrentStation():
    status = cmd("mpc")
    if "playing" in status:
        cs = cmd("mpc -f %position%")
        return int(cs)
    else:
        return 0


def stationPage(next):
    status = ""
    cs = getCurrentStation()
    if next:
        cs = cs + 10
        if cs > G_VAR["TOTAL_OF_QUEUE"]:
            cs = G_VAR["TOTAL_OF_QUEUE"]
        interuptDisplay(3, 15, "play pos " + str(cs))
        noReturnSubprocess(f"mpc play {cs}")
    else:
        cs = cs - 10
        if cs < 1:
            cs = 1
        interuptDisplay(3, 15, "play pos " + str(cs))
        noReturnSubprocess(f"mpc play {cs}")


def setVOL(up):
    status = ""
    vol = ""
    status = cmd(
        "mpc volume " + ("+5" if up else "-5") + " | grep volume | awk '{print$2}'"
    )
    interuptDisplay(3, 25, "v " + status)
    broadcast_message("vol=" + status)


def trackrepeat():
    RESULT = cmd("mpc repeat | grep -o 'repeat: \w\+' | awk '{print $2}'")  # toggle
    interuptDisplay(3, 15, "repeat " + RESULT)


def reboot():
    if G_VAR["TO_REBOOT"] is False:
        G_VAR["TO_REBOOT"] = True
        interuptDisplay(8, 16, "press again\nto reboot")
    else:
        interuptDisplay(3, 16, "rebooting...")
        sleep(1)
        os.system("reboot")


def exitset(info):
    G_VAR["SECOND_DIGIT"] = 0
    G_VAR["GOTOSTATION"] = False
    G_VAR["PICK_PLAYLIST"] = False
    G_VAR["TEN_PLUS"] = False
    G_VAR["NUM_VOL"] = 0
    G_VAR["STOP_SLEEP"] = False
    G_VAR["MINUTE_SLEEP"] = 0
    if info:
        interuptDisplay(3, 16, "operation\ncanceled")


def clickNum(pos):
    ypos = random.randint(0, 54)
    xpos = random.randint(0, 50)
    G_VAR["PULSE_COUNT"] = 0
    status = ""
    if (
        G_VAR["NUM_VOL"] == 0
        and G_VAR["MINUTE_SLEEP"] == 0
        and G_VAR["PICK_PLAYLIST"] is False
    ):
        if G_VAR["TOTAL_OF_QUEUE"] < 10:
            interuptDisplay(3, 15, "play pos " + str(pos))
            os.system("mpc play " + str(pos))
            return
        else:
            if G_VAR["SECOND_DIGIT"] > 0:
                G_VAR["SECOND_DIGIT"] += pos
                if G_VAR["SECOND_DIGIT"] > G_VAR["TOTAL_OF_QUEUE"]:
                    interuptDisplay(
                        3,
                        12,
                        "input out range\n"
                        + (f'{G_VAR["SECOND_DIGIT"]} in {G_VAR["TOTAL_OF_QUEUE"]}'),
                    )
                    G_VAR["SECOND_DIGIT"] = 0
                    return
                else:
                    interuptDisplay(3, 15, "play pos " + str(G_VAR["SECOND_DIGIT"]))
                    os.system("mpc play " + str(G_VAR["SECOND_DIGIT"]))
                    G_VAR["SECOND_DIGIT"] = 0
                    broadcast_message("resettimer")
                return
            else:
                interuptDisplay(3, 15, (f"play pos {str(pos)}_"))
                G_VAR["SECOND_DIGIT"] = pos * 10
                return
        return
    if G_VAR["NUM_VOL"] == 1:
        G_VAR["VOLTO"] = pos * 10
        interuptDisplay(5, 15, "volume to\n" + str(pos) + "x")
        print("start vol========== " + str(G_VAR["VOLTO"]))
        G_VAR["NUM_VOL"] = 2
        broadcast_message("resettimer")
    elif G_VAR["NUM_VOL"] == 2:
        G_VAR["VOLTO"] += pos
        G_VAR["NUM_VOL"] = 0
        interuptDisplay(5, 15, "set volume to\n" + str(G_VAR["VOLTO"]))
        os.system("mpc volume " + str(G_VAR["VOLTO"]))
        broadcast_message("resettimer")

    if G_VAR["MINUTE_SLEEP"] == 1:
        G_VAR["MIN_SLEEP_VALUE"] = 0
        G_VAR["MIN_SLEEP_VALUE"] = pos * 10
        interuptDisplay(5, 15, "sleep in\n" + str(pos) + "x minutes")
        G_VAR["MINUTE_SLEEP"] = 2
    elif G_VAR["MINUTE_SLEEP"] == 2:
        G_VAR["MIN_SLEEP_VALUE"] += pos
        interuptDisplay(
            8,
            13,
            "sleep in\n"
            + str(G_VAR["MIN_SLEEP_VALUE"])
            + " minutes\nClick OK to\nconfirm",
        )
    if G_VAR["PICK_PLAYLIST"] is True:
        status = cmd("mpc clear")
        sleep(0.1)
        if pos < len(PLAYlists) + 1:
            status = cmd("mpc load " + PLAYlists[pos - 1])
            getstationlen()
            status = status.replace(" ", "\n")
            interuptDisplay(2, 16, status)
            sleep(1)
            CONFIGDATA["curent_pl_id"] = pos
            G_VAR["PLAYLIST_POINTER"] = pos
            print(f'PLAYLIST_POINTER = {G_VAR["PLAYLIST_POINTER"]-1}/{len(PLAYlists)}')

            # with open(config_path, "w") as f:
            #     json.dump(CONFIGDATA, f, indent=4)
            save_config()
            status = cmd("mpc play")
            broadcast_message("info=" + status)
            display.frezeeDisplay(3)
        G_VAR["PICK_PLAYLIST"] = False


def switchPLAYLIST():
    G_VAR["PLAY_CURL"] = False
    getstationlen()
    if G_VAR["SWITCH_PLAYLIST"] is True:
        G_VAR["SWITCH_PLAYLIST"] = False
    else:
        G_VAR["SWITCH_PLAYLIST"] = True

    print("SWITCH_PLAYLIST=" + str(G_VAR["SWITCH_PLAYLIST"]))
    G_VAR["PLAYLIST_POINTER"] += 1
    print(f'PLAYLIST_POINTER = {G_VAR["PLAYLIST_POINTER"]-1}/{len(PLAYlists)}')
    if G_VAR["PLAYLIST_POINTER"] - 1 == len(PLAYlists):
        G_VAR["PLAYLIST_POINTER"] = 1
    G_VAR["NEXT_PLAYLIST"] = True
    G_VAR["PULSE_COUNT"] = 0
    interuptDisplay(2, 16, "select\n" + PLAYlists[G_VAR["PLAYLIST_POINTER"] - 1])


def load_playlist():
    status = cmd("mpc clear")
    sleep(0.1)
    status = cmd("mpc load " + PLAYlists[G_VAR["PLAYLIST_POINTER"] - 1])
    getstationlen()
    status = status.replace(" ", "\n")
    interuptDisplay(2, 16, status)
    sleep(1)
    CONFIGDATA["curent_pl_id"] = G_VAR["PLAYLIST_POINTER"]
    with open(config_path, "w") as f:
        json.dump(CONFIGDATA, f, indent=4)
    save_config()
    status = cmd("mpc play")
    broadcast_message("info=" + status)
    display.frezeeDisplay(3)


def getstationlen():  # get total playlist
    status = cmd("mpc playlist")
    if "radioislam" in status or "Rodja" in status:
        G_VAR["SWITCH_PLAYLIST"] = True
        print("SWITCH_PLAYLIST " + "True" if True else "False")
    T_LINES = status.count("\n")
    G_VAR["TOTAL_OF_QUEUE"] = T_LINES
    print("playlist=" + str(T_LINES))


def displaytooled(status):
    if "volume" not in status:
        return
    mlpl = 22  # maximum length per line
    if "[" not in status:
        return

    sm = ""
    text = ""
    inrep = status.index("repeat")
    status = status[:inrep]

    inbrace = status.index("[")
    station = status[:inbrace]
    if len(station) > 44:
        station = station[0:44]
    infolist = textwrap.wrap(station, mlpl)

    indvol = status.index("volume")
    indel = status.index("/") + 3
    state = status[inbrace:indel]
    state = state.replace("/", " - ")
    state = state.replace("#", " ")
    msglist = textwrap.wrap(state, mlpl)

    stvol = status[indvol:]

    msglist.append(stvol)
    for i in infolist:
        msglist.append(i)

    status = status.replace("(0%)", "")
    status = status.replace("(volume", "\nvolume")

    totline = len(msglist)
    sm = ""
    text = ""
    totpage = int(len(msglist) / 4)
    ttlline = 4 * totpage
    if totline > ttlline:
        totpage += 1  # get actual page

    for x in range(totline):
        sm = str(msglist[x])
        text += sm
        text += "\n"
    display.display(text, (0, 0))
    print("to display=" + text)


getPlayState()
getstationlen()


def restart():
    if G_VAR["TORESTART"] is False:
        G_VAR["TORESTART"] = True
        interuptDisplay(8, 16, "press again\nto reload\nprogram")
    else:
        interuptDisplay(3, 16, "reload...")
        sleep(1)
        os.execv(sys.executable, ["python"] + sys.argv)


def restart_app():
    if G_VAR["TO_RESTARTAPP"] is False:
        G_VAR["TO_RESTARTAPP"] = True
        interuptDisplay(8, 16, "press again\nto restart\napplication")
    else:
        interuptDisplay(3, 16, "restarting...")
        sleep(1)
        os.execv(sys.executable, ["python"] + sys.argv)


def msleep(minutes):
    sleeptimer.startcdown(minutes)


def ok():
    if G_VAR["MINUTE_SLEEP"] > 0:
        interuptDisplay(
            3,
            15,
            "starting sleep timer\nin " + str(G_VAR["MIN_SLEEP_VALUE"]) + " minutes",
        )
        broadcast_message(
            "info=starting sleep timer\nin "
            + str(G_VAR["MIN_SLEEP_VALUE"])
            + " minutes"
        )
        G_VAR["MINUTE_SLEEP"] = 0
        sleeptimer.startcdown(G_VAR["MIN_SLEEP_VALUE"])


def millis():
    return round(time.time() * 1000)


PREVMILL = 0


def validityremote(remotename):
    status = None
    for item in CONFIGDATA["remote"]:
        if item["name"] == remotename:
            status = item["enable"]
            break  # stop loop once found
    # print(f'{remotename} enable status: {status}')
    return status


def processIR(irval):
    if not validityremote("nexmedia"):
        print("remote disabled by config")
        return
    if irval == REMOTE_CODES["NEXMEDIA"]["KR_YELLOW"]:
        G_VAR["EN_NEXMEDIA_R"] = not G_VAR["EN_NEXMEDIA_R"]
        interuptDisplay(
            3,
            0,
            "REMOTE control\n" + ("unlocked" if G_VAR["EN_NEXMEDIA_R"] else "locked"),
        )
        return
    if G_VAR["EN_NEXMEDIA_R"]:
        for i in range(len(KR_nNUM)):
            if irval == KR_nNUM[i][1]:
                clickNum(KR_nNUM[i][0])
                break
        if irval == REMOTE_CODES["NEXMEDIA"]["KR_VOLUP"]:
            print("volume up")
            setVOL(True)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_VOLDOWN"]:
            setVOL(False)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_STUP"]:
            setSTATION(True)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_STDOWN"]:
            setSTATION(False)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_UP"]:
            setVOL(True)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_DOWN"]:
            print("DOWN")
            setVOL(False)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_RIGHT"]:
            print("right")
            setSTATION(True)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_LEFT"]:
            print("left")
            setSTATION(False)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_PLAY"]:
            print("play")
            noReturnSubprocess("mpc play")
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_PAUSE"]:
            interuptDisplay(3, 16, "PAUSE")
            noReturnSubprocess("mpc pause")
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_STOP"]:
            print("stop")
            interuptDisplay(3, 0, "STOP")
            os.system("mpc stop")
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_TV"]:
            print("tv")  # switch playlist
            switchPLAYLIST()
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_OPT"]:
            print("opt")  # start vol
            startVol()
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_MAIL"]:  # 10+
            print("mail")
            startTenPos()
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_POWER"]:  # 10+
            print("reboot")
            reboot()
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_SLEEP"]:
            startsetsleep()
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_OK"]:
            if G_VAR["MINUTE_SLEEP"] > 0:
                ok()
            else:
                print("enter")
                interuptDisplay(3, 16, "PLAY/\nPAUSE")
                noReturnSubprocess("mpc toggle")
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_EXIT"]:
            exitset(True)
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_MEDIA"]:
            startPlistTo()
        elif irval == REMOTE_CODES["NEXMEDIA"]["KR_TV"]:
            G_VAR["GOTOSTATION"] = True

    else:
        if irval[:2] == "41":
            interuptDisplay(3, 0, "unregistered key remote\nor this remote locked")


def processIRc(irval):
    if not validityremote("car"):
        print("remote disabled by config")
        return
    for i in range(len(KR_cNUM)):
        if irval == KR_cNUM[i][1]:
            clickNum(KR_cNUM[i][0])
            break
    if irval == REMOTE_CODES["KRC"]["KRC_VOLUP"]:
        print("volume up")
        setVOL(True)
    elif irval == REMOTE_CODES["KRC"]["KRC_VOLDOWN"]:
        setVOL(False)
    elif irval == REMOTE_CODES["KRC"]["KRC_STUP"]:
        setSTATION(True)
    elif irval == REMOTE_CODES["KRC"]["KRC_STDOWN"]:
        setSTATION(False)
    elif irval == REMOTE_CODES["KRC"]["KRC_PLAY"]:
        if G_VAR["MINUTE_SLEEP"] > 0:
            ok()
        else:
            print("play")
            os.system("mpc play")
    elif irval == REMOTE_CODES["KRC"]["KRC_MUTE"]:
        print("mute > stop")
        interuptDisplay(3, 0, "STOP")
        os.system("mpc stop")
    elif irval == REMOTE_CODES["KRC"]["KRC_MODE"]:
        print("mode > switch playlist")  # switch playlist
        switchPLAYLIST()
    elif irval == REMOTE_CODES["KRC"]["KRC_CALL"]:
        print("call > vol jump")  # start vol
        startVol()
    elif irval == REMOTE_CODES["KRC"]["KRC_CCALL"]:  # 10+
        print("ccall > ten+")
        startTenPos()
    elif irval == REMOTE_CODES["KRC"]["KRC_POWER"]:  # 10+
        print("reboot")
        reboot()
    elif irval == REMOTE_CODES["KRC"]["KRC_POWER"]:  # 10+
        print("get net data")
    elif irval == REMOTE_CODES["KRC"]["KRC_MENU"]:
        startsetsleep()


def processIRw(irval):
    if not validityremote("putih"):
        print("remote disabled by config")
    # if REMOTES[1]["enable"] is False:
    if CONFIGDATA["remote"][1]["enable"] is False:
        processIRe(irval)
        return
    else:
        for i in range(len(KR_wNUM)):
            if irval == KR_wNUM[i][1]:
                clickNum(KR_wNUM[i][0])
                break
        if irval == REMOTE_CODES["PUTIH"]["KW_VOLUP"]:
            print("volume up")
            setVOL(True)
        elif irval == REMOTE_CODES["PUTIH"]["KW_VOLDOWN"]:
            setVOL(False)
        elif irval == REMOTE_CODES["PUTIH"]["KW_STUP"]:
            setSTATION(True)
        elif irval == REMOTE_CODES["PUTIH"]["KW_STDOWN"]:
            setSTATION(False)
        elif irval == REMOTE_CODES["PUTIH"]["KW_ENTER"]:
            if G_VAR["MINUTE_SLEEP"] > 0:
                ok()
            else:
                print("enter")
                os.system("mpc toggle")
        elif irval == REMOTE_CODES["PUTIH"]["KW_PLAY"]:
            if G_VAR["MINUTE_SLEEP"] > 0:
                ok()
            else:
                print("play")
                os.system("mpc play")
        elif irval == REMOTE_CODES["PUTIH"]["KW_STOP"]:
            print("mute > stop")
            interuptDisplay(3, 0, "STOP")
            os.system("mpc stop")
        elif irval == REMOTE_CODES["PUTIH"]["KW_INPUT"]:
            print("mode > switch playlist")  # switch playlist
            switchPLAYLIST()
        elif irval == REMOTE_CODES["PUTIH"]["KW_SVOL"]:
            print("call > vol jump")  # start vol
            startVol()
        elif irval == REMOTE_CODES["PUTIH"]["KW_TEN"]:  # 10+
            print("ccall > ten+")
            startTenPos()
        elif irval == REMOTE_CODES["PUTIH"]["KW_POWER"]:  # 10+
            print("reboot")
            reboot()
        elif irval == REMOTE_CODES["PUTIH"]["KW_POWER"]:  # 10+
            print("get net data")
        elif irval == REMOTE_CODES["PUTIH"]["KW_SLEEP"]:
            startsetsleep()
        elif irval == REMOTE_CODES["PUTIH"]["KW_MUTE"]:
            restart()


def processIRe(irval):
    if not validityremote("evecross"):
        print("remote disabled by config")
        return
    print(f"irvaleu > {irval}")
    # if REMOTES[3]["enable"] is False:
    if CONFIGDATA["remote"][3]["enable"] is False:
        interuptDisplay(2, 10, "remote locked")
        return
    else:
        for i in range(len(KR_eNUM)):
            if irval == KR_eNUM[i][1]:
                clickNum(KR_eNUM[i][0])
                break
        if irval == REMOTE_CODES["EVERCROSS"]["KRE_VOLUP"]:
            print("volume up")
            setVOL(True)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_VOLDOWN"]:
            setVOL(False)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_STUP"]:
            setSTATION(True)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_STDOWN"]:
            setSTATION(False)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_OK"]:
            if G_VAR["MINUTE_SLEEP"] > 0:
                ok()
            else:
                print("enter")
                interuptDisplay(3, 16, "PLAY/\nPAUSE")
                noReturnSubprocess("mpc toggle")
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_PLAY"]:
            if G_VAR["MINUTE_SLEEP"] > 0:
                ok()
            else:
                print("play")
                interuptDisplay(3, 16, "PLAY")
                noReturnSubprocess("mpc play")
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_PAUSE"]:
            interuptDisplay(3, 16, "PAUSE")
            noReturnSubprocess("mpc pause")
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_STOP"]:
            print("mute > stop")
            interuptDisplay(3, 0, "STOP")
            os.system("mpc stop")
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_TV"]:
            print("mode > switch playlist")  # switch playlist
            switchPLAYLIST()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_RECALL"]:
            print("call > vol jump")  # start vol
            startVol()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_INFO"]:  # 10+
            print("ccall > ten+")
            startTenPos()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_POWER"]:  # 10+
            print("reboot")
            reboot()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_POWER"]:  # 10+
            print("get net data")
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_TIMER"]:
            startsetsleep()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_MUTE"]:
            restart()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_FAV"]:
            startPlistTo()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_EXIT"]:
            exitset(True)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_PAGEUP"]:
            display.setPage(True)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_PAGEDOWN"]:
            display.setPage(False)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_NEXT"]:
            stationPage(True)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_PREVIOUS"]:
            stationPage(False)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_FORWARD"]:
            seekthrough(True)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_REWIND"]:
            seekthrough(False)
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_GOTO"]:
            G_VAR["GOTOSTATION"] = True
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_SUB"]:
            restart_app()
        elif irval == REMOTE_CODES["EVERCROSS"]["KRE_REPEAT"]:
            trackrepeat()


settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


def broadcast_message(message):
    for client in WSHandler.clients:
        try:
            client.write_message(message)
        except Exception as e:
            print(f"error sending ws msg : {e}")


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
            G_VAR["MIN_SLEEP_VALUE"] = int(value)
            sleeptimer.startcdown(G_VAR["MIN_SLEEP_VALUE"])
            interuptDisplay(
                3,
                15,
                "starting sleep timer\nin "
                + str(G_VAR["MIN_SLEEP_VALUE"])
                + " minutes",
            )
            self.render("index.html")
            return
        if curlval != "":
            sleeptimer.resetAutoStop()
            if G_VAR["PLAY_CURL"] is False:
                status = cmd("mpc clear")
            sleep(0.1)
            status = cmd("mpc add " + curlval)
            interuptDisplay(2, 16, status)
            sleep(1)
            status = cmd("mpc play")
            displaytooled(status)
            broadcast_message("info=" + status)
            display.frezeeDisplay(3)
            G_VAR["PLAY_CURL"] = True
            self.render("index.html")


class SettingHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("settings.html")

    def post(self):
        try:
            data = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.set_status(400)  # Bad Request
            self.write({"error": "Invalid JSON"})
            return
        print("got post jremote")
        REMOTES = CONFIGDATA.get("remote", "")
        print("remote array: " + str(REMOTES))
        CONFIGDATA = data
        j = json.dumps(data)
        print(j)
        with open(config_path, "w") as f:
            json.dump(CONFIGDATA, f)


class shellCmd(tornado.web.RequestHandler):  # scmd
    def get(self, input):
        if input == "playlist":
            idd = 0
            # print(f'get play state: {getPlayState()}')
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
                if "://" in pl[i]:
                    pl[i] = pl[i][pl[i].index("//") + 2 :]
                mark = (
                    'id="playing" class="button1 bplay"'
                    if i + 1 == idd
                    else 'class="button1"'
                )
                rp += f"<button {mark} onclick=\"sendcmd('mpc play {i+1}')\"><a>{i+1}. {pl[i]}</a></button>"
            self.write(rp)
        elif input == "iplaylist":
            sr = subprocess.check_output("mpc lsplaylists", shell=True).decode("utf-8")
            pl = sr.splitlines(keepends=False)
            pl.sort()
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
            status = cmd("mpc")
            sr = status
            self.write(sr)
        elif input == "sttsjson":
            status = get_mpc_status()
            self.write(json.dumps(status))
        elif input == "config":
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(CONFIGDATA))
        elif input == "remotes":
            rp = ""
            for i in range(len(REMOTES)):
                benable = "" if REMOTES[i]["enable"] is False else 'checked="true"'
                rp += (
                    '<div id="state1" class="switch_led" style="margin: auto; padding: 8px" ><p4 id="swp1" style="font-size: 12px">'
                    + str(i + 1)
                    + ". "
                    + str(REMOTES[i]["name"])
                    + '</p4><label class="switchled"> <input type="checkbox" '
                    + benable
                    + ' id="remote'
                    + str(i + 1)
                    + '" value="'
                    + str(REMOTES[i]["name"])
                    + '" onchange="rchange('
                    + str(i + 1)
                    + ')"/> <span class="slider"></span></label> </div>'
                )
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(REMOTES))
        elif input == "hostname":
            sr = subprocess.check_output("hostname", shell=True).decode("utf-8")
            self.write(sr)
        elif input == "getsleep":
            sst = sleeptimer.update()
            self.write(sst)
        elif input == "stopsleep":
            sst = sleeptimer.stopcdown()
            self.write("timer stopped")
        elif input == "restart":
            print("This program will restart itself in 2 seconds...")
            interuptDisplay(8, 0, "Restarting app")
            time.sleep(0.5)
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


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
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
        print(f"[WS] Incoming message:{message}"), message

        if message.startswith("0>"):
            sbmsg = message[2:]
            if sbmsg.startswith("mpc"):
                sleeptimer.resetAutoStop()
                print("start with mpc")
            if sbmsg.startswith("mpc load"):
                subprocess.check_output("mpc clear", shell=True)
                subprocess.check_output(sbmsg, shell=True).decode("utf-8")
                subprocess.check_output("mpc play ", shell=True).decode("utf-8")
                for i in range(len(PLAYlists)):
                    if PLAYlists[i] in sbmsg:
                        CONFIGDATA["curent_pl_id"] = i + 1
                        G_VAR["PLAYLIST_POINTER"] = i + 1
                        save_config()
                        break
                G_VAR["PLAY_CURL"] = False
                interuptDisplay(3, 16, "switcing PLAYlists")
            elif sbmsg.startswith("mpc volume"):
                out = cmd(sbmsg + " | grep volume | awk '{print$2}'")
                interuptDisplay(3, 25, "v " + out)
            else:
                sr = cmd(sbmsg)
                print("incoming ws msg: " + sr)
                interuptDisplay(3, 16, sr)
        elif message.startswith("1>"):
            sbmsg = message[2:]
            if sbmsg.startswith("stopsleep"):
                sleeptimer.stopcdown()

    @classmethod
    async def send_message(cls, message):
        for client in cls.clients:
            if client.ws_connection:
                try:
                    await client.write_message(message)
                except Exception as e:
                    print(f"error sending ws msg : {e}")


class SerialReader(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        global serial_transport
        serial_transport = transport
        print("Serial port opened", transport)

    def data_received(self, data):
        message = data.decode("utf-8").strip()
        serial_write(message)
        print(f"Received from serial: {message}")
        ss = message[:2]
        if ss == "FF":
            processIRc(message)
            sleeptimer.resetAutoStop()
        elif ss == "41":
            processIR(message)
            sleeptimer.resetAutoStop()
        elif ss == "FD":
            processIRw(message)
            sleeptimer.resetAutoStop()

    def connection_lost(self, exc):
        print("Serial port closed")
        asyncio.get_event_loop().stop()


async def start_serial_reader(port, baudrate):
    loop = asyncio.get_event_loop()
    await serial_asyncio.create_serial_connection(loop, SerialReader, port, baudrate)


def serial_write(msg):
    if serial_transport is not None:
        print(f"Sending to serial: {msg}")
        serial_transport.write(msg.encode())
    else:
        print("Serial port not connected.")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/scmd/(\w+)", shellCmd),
            (r"/websocket", WSHandler),
            (r"/settings", SettingHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"}),
        ],
        **settings,
    )


def broadcast_rplist():
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
    if rp != G_VAR["PREV_PLAYLIST"]:
        G_VAR["PREV_PLAYLIST"] = rp
        broadcast_message("pls=" + rp)


def infinity():
    G_VAR["SCOUNT"] += 1
    if G_VAR["SCOUNT"] % 2 == 0:
        broadcast_rplist()
    if G_VAR["SCOUNT"] == 10:
        G_VAR["SCOUNT"] = 0
    status = (
        subprocess.check_output("mpc current", shell=True)
        .decode("utf-8")
        .replace("\n", "")
    )
    if status != G_VAR["PREV_STATUS"]:
        try:
            broadcast_message("info=" + status + ">__ws")
        except Exception as e:
            print(f"error sending ws msg : {e}")
    G_VAR["PREV_STATUS"] = status


def signal_handler(sig, frame):
    print("Signal received, cancelling tasks...")
    for task in asyncio.all_tasks():
        task.cancel()


async def secondy():
    while True:
        loop()
        sleeptimer.beat()
        await asyncio.sleep(1)


async def tick():  # 100ms pulse
    while True:
        infinity()
        G_VAR["PULSE_COUNT"] += 1
        if G_VAR["PULSE_COUNT"] > 15:
            G_VAR["PULSE_COUNT"] = 0
            if G_VAR["SECOND_DIGIT"] > 0:
                G_VAR["SECOND_DIGIT"] = int(G_VAR["SECOND_DIGIT"] / 10)
                os.system("mpc play " + str(G_VAR["SECOND_DIGIT"]))
                G_VAR["SECOND_DIGIT"] = 0
            elif G_VAR["NEXT_PLAYLIST"] is True:
                load_playlist()
                G_VAR["NEXT_PLAYLIST"] = False
        await asyncio.sleep(0.1)


async def iorun():
    print("iorun")
    await tick()


port = "/dev/ttyS5"
baudrate = 9600

app = make_app()
app.listen(8888)
try:
    asyncio.ensure_future(start_serial_reader(port, baudrate))
    print("after ensure_future")
    asyncio.ensure_future(tick())
    asyncio.ensure_future(secondy())
    tornado.ioloop.IOLoop.current().start()
    print("after tornado.IO")
except KeyboardInterrupt:
    sleep(1)
    print("Keyboard interrupt received, exiting...")
