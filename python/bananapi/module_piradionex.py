#!/usr/bin/python
import serial
import serial.tools.list_ports
from time import sleep

import textwrap
import subprocess
import random
import threading
import json
import os
import math
import psutil
import mpcstimer
import re

stimer = mpcstimer.mpctimer()

import Nextiondisplay

MyNextion = Nextiondisplay.display()

local_ip = ""
NETSTAT = ""

cputemp = ""

CDOWN = False
T_ENABLE = False
SEC_CD = 0
ON_MENU = False
ASCDOWN = True
ASSECCD = 0
PLAYING = True
ASSECMX = 3600
nextion_page = 4
RADIO_STATUS = {}
BLANK_SCREEN = 0
TOBLANKSCREEN = False

stationAlternative = {"My Station name": "Hang FM Batam"}


def send_wall_message(message: str):
    try:
        # Send the message using the 'wall' command
        subprocess.run(["wall"], input=message.encode(), check=True)
        print("Message sent to all logged-in users.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send message: {e}")


def GreenYellowRed(value):
    # Clamp the value to be between 0 and 100
    # and map to green > yellow> red
    value = max(0, min(100, value))

    # Calculate the red and green components
    # red = int((value / 100) * 255)  # Scale to 0-255
    red = 255
    if value < 51:
        red = map_value(value, 0, 50, 0, 255)
    green = 255
    if value > 50:
        green = map_value(value, 50, 100, 255, 0)
    # print(f'v:{value} r:{red} g:{green}')
    # Convert to RGB565
    r_565 = (red >> 3) & 0x1F  # 5 bits for red
    g_565 = (green >> 2) & 0x3F  # 6 bits for green
    b_565 = 0  # Blue is always 0 in this gradient

    # Combine into a single 16-bit value
    rgb565 = (r_565 << 11) | (g_565 << 5) | b_565
    return rgb565


def RedYellowGreen(value):
    # Clamp the value to be between 0 and 100
    # and map to red > yellow> green
    value = max(0, min(100, value))

    # Calculate the red and green components
    # red = int((value / 100) * 255)  # Scale to 0-255
    green = 255
    if value < 51:
        green = map_value(value, 0, 50, 0, 255)
    red = 255
    if value > 50:
        red = map_value(value, 50, 100, 255, 0)
    # print(f'v:{value} r:{red} g:{green}')
    # Convert to RGB565
    r_565 = (red >> 3) & 0x1F  # 5 bits for red
    g_565 = (green >> 2) & 0x3F  # 6 bits for green
    b_565 = 0  # Blue is always 0 in this gradient

    # Combine into a single 16-bit value
    rgb565 = (r_565 << 11) | (g_565 << 5) | b_565
    return rgb565


def map_value(src, in_from, in_to, outfrom, out_to):
    if src < in_from or src > in_to:
        raise ValueError(f"Value {src} is out of range [{in_from}, {in_to}]")
    return int(outfrom + (src - in_from) * (out_to - outfrom) / (in_to - in_from))


def nexinit():
    # global nextion_page
    MyNextion.set_port("/dev/ttyS1")
    # MyNextion.send_command('page page2')#sukses
    MyNextion.send_command("page 4")  # sukses
    # MyNextion.send_command("dim=10")  # sukses
    nextion_page = 4
    # MyNextion.send_command('t1.bco=BLUE')# sukses
    result = subprocess.check_output("hostname", shell=True).decode("utf-8")
    if "\n" in result:
        result = result.replace("\n", "")
    MyNextion.send_command(f't0.txt="{result} radio"')
    sr = subprocess.check_output("mpc current", shell=True).decode("utf-8")
    MyNextion.send_command(f't1.txt="{sr}"')  # station name
    MyNextion.send_command("t1.isbr=1")  # sukses 1=true 0=false
    MyNextion.send_command("t1.xcen=Center")

    MyNextion.send_command("t10.xcen=1")  # data received
    MyNextion.send_command("t10.ycen=1")  # data received

    MyNextion.send_command("h0.bco=65535")  # white
    MyNextion.send_command("h0.val=34")  # vol
    ct = GreenYellowRed(42)
    # MyNextion.send_command('j3.bco=65535')#white
    MyNextion.send_command(f"j3.pco={ct}")  # cpu temp
    MyNextion.send_command("j3.val=42")  # cpu temp
    cpuload = random.randint(0, 101)
    memload = random.randint(0, 101)
    ml = GreenYellowRed(memload)
    MyNextion.send_command(f"j1.pco={ml}")  # memory load
    MyNextion.send_command(f"j1.val={memload}")  # memory load

    MyNextion.send_command("t2.isbr=1")  # sukses 1=true
    MyNextion.send_command("t2.ycen=1")
    MyNextion.send_command('t2.txt="radio starting..."')  # log
    local_ip = ""
    cmd = "hostname -I | awk '{print$1}'"
    result = subprocess.check_output(cmd, shell=True)
    local_ip = result.decode("utf-8")
    MyNextion.send_command(f't3.txt="{local_ip}"')  # ip
    MyNextion.send_command('t4.txt="3"')  # station index


nexinit()  # setup nextion


class sleeptimer:
    def startcdown(self, minutes):
        global T_ENABLE, SEC_CD
        T_ENABLE = True
        SEC_CD = minutes * 60
        print("sleep timer just started")
        return

    def stopcdown(self):
        global T_ENABLE, SEC_CD
        T_ENABLE = False
        SEC_CD = 0
        MyNextion.send_command("sleep timer stopped by user")
        print("sleep timer stopped by user")
        return

    def countdown(self):
        global T_ENABLE
        global SEC_CD
        # print("sec cd = "+str(SEC_CD))
        if T_ENABLE is True and PLAYING is True:
            mins, secs = divmod(SEC_CD, 60)
            timer = f"{mins:02d}:{secs:02d}"
            # print(f'Time left: {timer}', end='\r')
            SEC_CD -= 1
            # print(SEC_CD)
            if SEC_CD == 0:
                print("\nTime's up!")
                os.system("mpc stop")
                MyNextion.send_command(
                    't2.txt="player stopped due timer defined by user"'
                )
                T_ENABLE = False
                # quit()

    # auto stop reset counting
    def resetas(self):
        global ASSECCD
        global nextion_page
        global BLANK_SCREEN
        ASSECCD = 0
        BLANK_SCREEN = 0
        if nextion_page == 0:
            nextion_page = 4
            MyNextion.send_command("page 4")
            # MyNextion.send_command("dim=30")
            MyNextion.send_command("t1.isbr=1")  # sukses 1=true 0=false
            MyNextion.send_command("t1.xcen=Center")

    # get auto stop second running
    def getsecac(self):
        return str(ASSECCD)

    def autostop(self):
        global ASSECCD#, ASCDOWN, ASSECMX
        global BLANK_SCREEN, TOBLANKSCREEN
        # BLANK_SCREEN = 0
        TOBLANKSCREEN = False
        if ASCDOWN is True and PLAYING is True:
            ASSECCD += 1
            # print("serial display auto stop  "+str(ASSECCD))
            if ASSECCD == ASSECMX:
                print("\nauto stop due a 1 hour no user activity!")
                send_wall_message("mpc stopped due 1 hour without user control")
                MyNextion.send_command(
                    't2.txt="auto stop due a 1 hour no user activity!"'
                )
                TOBLANKSCREEN = True
                os.system("mpc stop")
            elif ASSECCD > (ASSECMX + 1):
                ASSECCD = ASSECMX + 1


    def toblank(self):
        global BLANK_SCREEN
        global TOBLANKSCREEN
        global nextion_page
        if TOBLANKSCREEN is True :
            BLANK_SCREEN += 1
            if BLANK_SCREEN == 300:
                MyNextion.send_command("page 0")
                nextion_page = 0
                MyNextion.send_command("dim=0")
                TOBLANKSCREEN = False
            elif BLANK_SCREEN > 300:
                BLANK_SCREEN = 301
        if RADIO_STATUS["is_playing"] is False:
            BLANK_SCREEN += 1
            if BLANK_SCREEN == 300:
                MyNextion.send_command("page 0")
                nextion_page = 0
                MyNextion.send_command("dim=0")
                TOBLANKSCREEN = False
            elif BLANK_SCREEN > 300:
                BLANK_SCREEN = 301

    def loopy(self):
        # self.cekStart()
        # self.cekStop()
        self.countdown()
        self.autostop()
        self.toblank()
        # threading.Timer(1, loopy).start()  # Schedule the function to run again in 1 second

    def isrunning(self):
        global T_ENABLE
        return T_ENABLE

    def update(self):
        #global T_ENABLE
        #global SEC_CD
        # print("sec cd = "+str(SEC_CD))
        if T_ENABLE is True:
            mins, secs = divmod(SEC_CD, 60)
            hours, mins = divmod(mins, 60)
            timer = f"{hours:02d}:{mins:02d}:{secs:02d}"
            return "sleep in > " + str(timer)
        else:
            return "off"


msleeptimer = sleeptimer()


def load_variable():
    global SEC_CD
    global T_ENABLE
    try:
        with open("/home/timer.json", "r") as f:
            data = json.load(f)
            T_ENABLE = data.get("enable", False)
            SEC_CD = data.get("seconds", 120)
    except FileNotFoundError:
        pass


def getlocal_ip():
    global local_ip
    cmd = "hostname -I | awk '{print$1}'"
    result = subprocess.check_output(cmd, shell=True)
    local_ip = result.decode("utf-8")
    if ":" in local_ip:
        local_ip = local_ip[: (local_ip.index(":") - 5)]
        # print("ipv6 exist")
        # print("length ip"+str(len(local_ip)))
        # local_ip=local_ip.rstrip
        # local_ip=local_ip.replace("\n", "")
    else:
        local_ip = local_ip[: len(local_ip) - 1]
        # print("length ip"+str(len(local_ip)))
    local_ip = "IP: " + local_ip
    print(local_ip)


getlocal_ip()


def updateCPUtemp():
    global cputemp
    cmd = "cat /sys/class/thermal/thermal_zone0/temp"
    result = subprocess.check_output(cmd, shell=True)
    iict = int(result.decode("utf-8")) / 1000
    ict = int(iict)
    ct = GreenYellowRed(ict)
    MyNextion.send_command(f"j3.pco={ct}")  # cpu temp
    MyNextion.send_command(f"j3.val={ict}")  # cpu temp
    # print(f'h1.val={ict}')
    cputemp = "cpu temp: " + result.decode("utf-8")[:2] + "c"
    # print(cputemp)


def sysinfo():
    sinfo = ""
    cpu_percent = psutil.cpu_percent(interval=None)
    sinfo = f"CPU: {cpu_percent}% "
    cpul = int(cpu_percent)
    # print(f'h1.val={cpul}')
    cl = GreenYellowRed(cpul)
    MyNextion.send_command(f"j0.pco={cl}")  # cpu load
    MyNextion.send_command(f"j0.val={cpul}")  # cpu load

    memory_usage = psutil.virtual_memory()
    sinfo += f"Mem: {memory_usage.percent}%"
    memload = int(memory_usage.percent)
    ml = GreenYellowRed(memload)
    MyNextion.send_command(f"j1.pco={ml}")  # cpu temp
    MyNextion.send_command(f"j1.val={memload}")  # memory load

    return sinfo


net_io = psutil.net_io_counters()
initial_bytes_sent = net_io.bytes_sent
initial_bytes_recv = net_io.bytes_recv
final_bytes_sent = net_io.bytes_sent
final_bytes_recv = net_io.bytes_recv


def getnspeed():
    global initial_bytes_sent
    global initial_bytes_recv
    global final_bytes_sent
    global final_bytes_recv

    net_io = psutil.net_io_counters()
    final_bytes_sent = net_io.bytes_sent
    final_bytes_recv = net_io.bytes_recv

    # Calculate the speed
    sent_speed = (final_bytes_sent - initial_bytes_sent) / 1024  # Convert to KB
    recv_speed = (final_bytes_recv - initial_bytes_recv) / 1024  # Convert to KB

    net_io = psutil.net_io_counters()
    initial_bytes_sent = net_io.bytes_sent
    initial_bytes_recv = net_io.bytes_recv

    return sent_speed, recv_speed


P_COUNT = 0


def displaytooled(status):
    global local_ip
    global NETSTAT
    if len(local_ip) < 8:
        getlocal_ip()

    mlpl = 21  # maximum length per line
    mlpp = 5  # maximum line per page
    # srink status
    inrep = status.index("repeat")
    status = status[:inrep]

    # crop station info
    inbrace = status.index("[")
    station = status[:inbrace]
    if station in stationAlternative:
        station = stationAlternative[station]
    MyNextion.send_command(f't1.txt="{station}"')
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
    # print(f'stvol={stvol}')
    intvol = int(stvol[7 : stvol.index("%")])
    # print(f'intvol={intvol}')
    rv = GreenYellowRed(intvol)
    MyNextion.send_command(f"h0.bco1={rv}")  # cpu temp
    MyNextion.send_command(f"h0.val={intvol}")  # vol
    get_mpc_status()
    if RADIO_STATUS["time"]["total_seconds"] > 0:
        MyNextion.send_command(f"h1.val={RADIO_STATUS['progress_percent']}")
    else:
        MyNextion.send_command(f"h1.val={RADIO_STATUS['progress_percent']}")

    MyNextion.send_command(f"c0.val={'0' if not RADIO_STATUS['repeat'] else '1'}")
    MyNextion.send_command(f"c1.val={'0' if not RADIO_STATUS['random'] else '1'}")
    MyNextion.send_command(f"c2.val={'0' if not RADIO_STATUS['single'] else '1'}")
    MyNextion.send_command(f"c3.val={'0' if not RADIO_STATUS['consume'] else '1'}")

    # crop station index
    # print("state = " + state)
    STIDX = status[status.index("#") + 1 :]

    STIDX = STIDX[: STIDX.index(" ")]
    MyNextion.send_command(f't4.txt="{STIDX}"')  # station index
    for i in infolist:
        msglist.append(i)

        # msglist.append(i)
    msglist.append(stvol)
    msglist.append(local_ip)
    # msglist.append("test")
    msglist.append(NETSTAT)

    MyNextion.send_command(f't10.txt="{NETSTAT}"')
    msglist.append(cputemp)
    status = status.replace("(0%)", "")
    status = status.replace("(volume", "\nvolume")

    # load_variable()
    if T_ENABLE is True:
        # if stimer.isrunning() is True:
        mins, secs = divmod(SEC_CD, 60)
        hours, mins = divmod(mins, 60)
        timer = f"{hours:02d}:{mins:02d}:{secs:02d}"
        sst = "sleep in : " + timer
        # sst="sleep in : "+stimer.update()
        msglist.append(sst)
        # MyNextion.send_command(f't2.txt="{sst}"')
        MyNextion.send_command(f't3.txt="{sst}"')  # ip
    # myoled.display(status, (0,0))
    else:
        if len(local_ip) < 4:
            getlocal_ip()
        MyNextion.send_command(f't3.txt="{local_ip}"')  # ip

    # myoled.showmsg(status)
    msglist.append(sysinfo())
    totline = len(msglist)
    # print(totline)
    sm = ""
    text = ""
    totpage = int(len(msglist) / mlpp)
    ttlline = 4 * totpage
    if totline > ttlline:
        totpage += 1  # get actual page

    # print("total dirt line = " + str(ttlline))
    # print(totpage)

    global P_COUNT

    #    print("P_COUNT = " + str(P_COUNT))
    # for x in range(4):
    #     print(' '.join(msglist))
    # # for x in msglist:
    #     # text+=str(msglist[x])
    #     sm=str(msglist[x])
    #     text += sm
    #     serialdisplay(text)
    # text=(' '.join(msglist))

    for x in range(mlpp):
        idx = (P_COUNT * mlpp) + x
        if idx < totline:
            sm = str(msglist[idx])
            text += sm
            text += "\n"
        else:
            break

    # print(text)
    # myoled.display(text, (0,0))
    # data= str.encode(text)
    # con.write(data)
    # serialdisplay(text)
    # send_message(port_to_use, text)
    text = ""
    P_COUNT += 1
    if P_COUNT > (totpage - 1):
        P_COUNT = 0


old_station = ""
old_vol = ""


def anychange(status):
    change = False
    if "playing" in status or "paused" in status:
        global old_station
        global old_vol
        # srink status
        inrep = status.index("repeat") - 4
        status = status[:inrep]

        # crop station info
        inbrace = status.index("[")
        station = status[:inbrace]
        # print("station = " + station)
        # split limited length char to list

        # crop playing info
        indvol = status.index("volume")
        indel = status.index("/0")
        state = status[inbrace:indel]
        state = state.replace("#", " ")
        # split limited length char to list

        # crop volume info
        stvol = status[indvol + 8 :]

        # print("stvol"+stvol)
        if station != old_station:
            change = True
            print("station change")

        if stvol != old_vol:
            change = True
            print("volume change")
        # print("state = " + state)
        old_station = station
        old_vol = stvol
    return change


def getNetData():
    # required intall netstat
    global NETSTAT
    OUT = subprocess.check_output(
        "netstat -e -n -i | grep wlan0  -A 10 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'",
        shell=True,
    )
    NETSTAT = str(OUT)
    sbr = NETSTAT.index("(") + 1
    ebr = NETSTAT.index(")")
    # NETSTAT = "RX = " + NETSTAT[sbr:ebr]
    NETSTAT = NETSTAT[sbr:ebr]
    NETSTAT = NETSTAT.replace("i", "")

    dbm = subprocess.check_output(
        "/usr/sbin/iwconfig wlan0 | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2",
        shell=True,
    )
    signal = dbm.decode("utf-8")
    NETSTAT = NETSTAT  # + signal[1:]
    dbtopercent(dbm)
    # NETSTAT = NETSTAT + dbtopercent(dbm) #+ signal[1:]


def dbtopercent(value):
    inval = int(value)
    if inval != 0:
        # percent = 100 * (1 - ((-1) - inval) / ((-1)- (-98)))
        # percent =max(0, min(100, (inval + 100) * 100 / 50))

        # percent =max(0, min(100, (inval + 100) * 100 / 50))

        maxdb = -20
        mindb = -100  # signal parameter in dbm
        percent = int(0 + (inval - (mindb)) * (100 - 0) / ((maxdb) - (mindb)))
        pct = math.floor(percent)

        cl = RedYellowGreen(pct)
        # print(f'pct: {pct}')
        MyNextion.send_command(f"j2.pco={cl}")  # cpu temp\
        MyNextion.send_command(f"j2.val={pct}")
        # pct=pct[:]
        # print("percent="+pct)
        return "\nWiFi signal: " + str(pct) + "%"
    else:
        return "\nWiFi signal: 0%"


U_COUNT = 20
MAXUCOUNT = 22
STOP_COUNT = 0
SCREEN_SLEEP = False


def loop():
    global U_COUNT
    global MAXUCOUNT
    global STOP_COUNT
    global P_COUNT
    global SCREEN_SLEEP
    global PLAYING
    global nextion_page
    global BLANK_SCREEN
    old_status = ""
    status = ""
    sent, recv = getnspeed()
    # print(f"Sent: {sent:.2f} KB/s, Received: {recv:.2f} KB/s")
    MyNextion.send_command(
        f't12.txt=" D: {recv:.2f} KB/s - U: {sent:.2f} KB/s"'
    )  # station index
    # os.system("mpc > tmp")
    # print(status)
    # if status != old_status:
    # if anychange(status) is True:
    #     if SCREEN_SLEEP is True:
    #         print("wake up oled")
    #         SCREEN_SLEEP = False
    #         myoled.show()
    #     P_COUNT = 0
    #     U_COUNT= 0
    # stimer.loopy()
    # print(stimer.update())
    # print("U_COUNT" + str(U_COUNT))
    if ON_MENU is False:
        status = subprocess.check_output("mpc", shell=True)
        status = status.decode("utf-8")
        if "playing" in status or "paused" in status:
            PLAYING = True
        else:
            PLAYING = False
        if U_COUNT == 20:
            if nextion_page != 4 and BLANK_SCREEN ==0:
                nextion_page = 4
                MyNextion.send_command("page 4")  # sukses
                MyNextion.send_command('t0.txt="banana radio"')
            if "playing" in status or "paused" in status:
                # data= str.encode(status)
                # serialdisplay(status)
                displaytooled(status)
                # print("loopy")
                # MAXUCOUNT=22
                STOP_COUNT = 0

            else:
                # myoled.clear(1)
                # MAXUCOUNT = 20
                STOP_COUNT += 1
                if STOP_COUNT == 1:
                    MyNextion.send_command('t1.txt="player stopped"')
                    MyNextion.send_command(f't3.txt="{local_ip}"')  # ip
                # print("STOP_COUNT" + str(STOP_COUNT))
                if STOP_COUNT > 50:
                    STOP_COUNT = 51
        U_COUNT += 1
        # if U_COUNT == 25:
        # NETSTAT =  status.decode("utf-8")
        if U_COUNT > MAXUCOUNT:
            getNetData()
            updateCPUtemp()
            U_COUNT = 20
        old_status = status

    msleeptimer.loopy()

    # threading.Timer(1, loop).start()  # Schedule the function to run again in 1 second


# loop()


class looptimer:
    """
    A timer that repeatedly calls a function in a separate thread.
    It can be started and stopped gracefully.
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._stop_event = threading.Event()
        self._timer = None

    def _run(self):
        """The core execution loop."""
        # Schedule the next run as long as the stop event is not set
        if not self._stop_event.is_set():
            self._function(*self._args, **self._kwargs)
            # Create and start the next timer
            self._timer = threading.Timer(self._interval, self._run)
            self._timer.start()

    def start(self):
        """Starts the timer loop."""
        if self.is_running():
            print("Timer is already running.")
            return

        print("Starting timer.")
        # Create the first timer and start the loop
        self._timer = threading.Timer(self._interval, self._run)
        self._timer.start()

    def stop(self):
        """Stops the timer loop gracefully."""
        if not self.is_running():
            print("Timer is not running.")
            return

        print("Stopping timer.")
        # Set the event to signal the loop to stop
        self._stop_event.set()
        # Cancel the next scheduled run, if any
        if self._timer:
            self._timer.cancel()
        print("Timer stopped.")

    def is_running(self):
        """Check if the timer is currently active."""
        return self._timer is not None and self._timer.is_alive()


class tasktimer:
    def start(self):
        self.timer_loop = looptimer(1, loop)
        self.timer_loop.start()

    def stop(self):
        self.timer_loop.stop()


# print("after loop")
#
class display:
    def resettimer(self):
        global U_COUNT
        U_COUNT = 19
        # print("reset timer")
        return

    def frezeeDisplay(self, delay):
        global U_COUNT
        global P_COUNT
        P_COUNT = 0
        U_COUNT = 20 - delay
        print("reset timer for " + str(delay))
        return

    def sendCommand(self, msg):
        MyNextion.send_command(msg)
        return

    def setPage(self, page):
        global nextion_page
        nextion_page = page
        # MyNextion.send_command(f"page page{page}")
        return

    def display(self, msg, pos):
        # myoled.display(msg, pos)
        # serialdisplay(msg)
        # send_message(port_to_use, msg)
        MyNextion.send_command('t2.txt="{msg}"')
        return

    def display(self, msg, rndom):
        mx = 128 - len(msg) * 6
        ypos = random.randint(0, 54) if rndom else 0
        xpos = random.randint(0, mx) if rndom else 0
        # myoled.display(msg, (xpos,ypos))
        # serialdisplay(msg)
        # send_message(port_to_use, msg)
        MyNextion.send_command(f't2.txt="{msg}"')
        return

    def onmenu(self, onmenu):
        global ON_MENU
        ON_MENU = onmenu
        return

    def getmenu(self):
        global ON_MENU
        return ON_MENU
    def reinit(self):
        nexinit()
        return
 

# class mpc_status():
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


def seconds_to_hms(sec: int) -> str:
    """Convert seconds to hh:mm:ss format"""
    if sec < 0:
        sec = 0
    h, m = divmod(sec, 3600)
    m, s = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}"


def get_mpc_status():
    #global ASSECCD
    #global ASCDOWN
    #global SEC_CD, T_ENABLE
    result = subprocess.run(["mpc", "status"], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()

    if not lines:
        return {"error": "mpc returned no output (MPD might not be running)"}

    global RADIO_STATUS
    # msleeptimer.update()
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
                "consume": False,
            }
        )
        volume_match = re.search(r"volume:\s*(\d+)%", lines[0])
        RADIO_STATUS["volume"] = int(volume_match.group(1)) if volume_match else None

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
                "enable": T_ENABLE,
                "second_countdown": SEC_CD,
                "countdown": (seconds_to_time(SEC_CD) if T_ENABLE else "off"),
                "auto_stop": {
                    "enable": ASCDOWN,
                    "second_countdown": ASSECCD,
                    "second_max": ASSECMX,
                    "countdown": (
                        seconds_to_hms(ASSECMX - ASSECCD) if ASCDOWN else "off"
                    ),
                },
            }
        }
    )
    return RADIO_STATUS
