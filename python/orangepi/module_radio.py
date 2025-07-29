#!/usr/bin/env python3

import os
import oledis
import textwrap
import subprocess
import random
import threading
from time import sleep
# import mpcstimer
import math
import json
import psutil

myoled= oledis.oled()
# stimer=mpcstimer.mpctimer()
local_ip = "192.168.1.123"
cputemp=""
NETSTAT = "0MB"
systemReady=0

CDOWN = False
T_ENABLE= False
SEC_CD = 0
ASCDOWN=True
ASSECCD=0
PLAYING= True
ASSECMX=3600



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
    cmd= "hostname -I | awk '{print$1}'"
    result= subprocess.check_output(cmd, shell=True)
    local_ip =  result.decode("utf-8")
    if ":" in local_ip:
        local_ip=local_ip[:(local_ip.index(":")-4)]
        # local_ip=local_ip.rstrip
        # local_ip=local_ip.replace("\n", "")
    local_ip=local_ip.replace("\n", "")
    local_ip = "IP: " + local_ip
    print(local_ip)
getlocal_ip()

def updateCPUtemp():
    global cputemp
    cmd= "cat /sys/class/thermal/thermal_zone0/temp"
    result= subprocess.check_output(cmd, shell=True)
    cputemp =  "cpu temp: "+result.decode("utf-8")[:2] + "c"
    # print(cputemp)


def sysinfo():
    sinfo=""
    cpu_percent = psutil.cpu_percent(interval=1)
    sinfo=(f"CPU: {cpu_percent}% ")
    memory_usage = psutil.virtual_memory()
    sinfo+=(f"Mem: {memory_usage.percent}%")
    return sinfo
# getlocal_ip()
P_COUNT=0
def displaytooled(status):
    global T_ENABLE
    global SEC_CD
    global local_ip
    global NETSTAT
    if len(local_ip) < 8:
        getlocal_ip()

    mlpl = 22# maximum length per line
    #srink status
    if "repeat" in status:
        inrep = status.index("repeat")
        status= status[:inrep]

        # crop station info
        inbrace =status.index("[")
        station = status[:inbrace]
        # print("station = " + station)
        # split limited length char to list
        infolist=textwrap.wrap(station, mlpl)

        # crop playing info
        indvol=status.index("volume")
        indel=status.index("(")-1
        state=status[inbrace:indel]
        state=state.replace("#", " ")
        if "0:00" in state:
            state=state.replace("[", "")
            state=state.replace("]", "")
            state=state.replace("/0:00", "")
        # split limited length char to list
        msglist=textwrap.wrap(state, mlpl)

        #crop volume info
        stvol=status[indvol:]

        # print("state = " + state)

        for i in infolist:
            msglist.append(i)

            # msglist.append(i)
        msglist.append(stvol)


    # load_variable()
    if T_ENABLE is True:
    # if stimer.isrunning() is True:
        mins, secs = divmod(SEC_CD, 60)
        hours, mins = divmod(mins, 60)
        timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
        sst="sleep in : "+ timer
        # sst="sleep in : "+stimer.update()
        msglist.append(sst)
    msglist.append(local_ip)
    #msglist.append("test")
    msglist.append(NETSTAT)
    msglist.append(cputemp)

    status= status.replace("(0%)", "")
    status= status.replace("(volume", "\nvolume")

    # myoled.display(status, (0,0))

    #myoled.showmsg(status)

    msglist.append(sysinfo())
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

    global P_COUNT

#    print("P_COUNT = " + str(P_COUNT))
    for x in range(4):
        idx=(P_COUNT*4)+x
        if idx < totline:
            sm=str(msglist[idx])
            text += sm
            text +="\n"
        else:
            break

        # print(text)
    myoled.display(text, (0,0))
    text=""
    P_COUNT+=1
    if P_COUNT > (totpage-1):
        P_COUNT=0

def displaytooled2():
    global T_ENABLE
    global SEC_CD
    global local_ip
    global NETSTAT
    if len(local_ip) < 8:
        getlocal_ip()

    mlpl = 22# maximum length per line

    status=subprocess.check_output("mpc", shell=True).decode("utf-8")

    #srink status
    if "repeat" in status:
        station=subprocess.check_output("mpc current", shell=True).decode("utf-8")
        # station=station.decode("utf-8")
        # print("station = " + station)
        # split limited length char to list
        infolist=textwrap.wrap(station, mlpl)

        # crop playing info
        state=subprocess.check_output("mpc | awk 'NR==2 {print$1$2}'", shell=True).decode("utf-8").replace("\n","")
        # print("state"+state+">")
        # state=state.decode("utf-8")
        state=state.replace("#", " ")
        # split limited length char to list
        msglist=textwrap.wrap(state, mlpl)

        #crop volume info
        stvol=subprocess.check_output("mpc volume", shell=True).decode("utf-8").replace("\n","")

        # print("state = " + state)

        for i in infolist:
            msglist.append(i)

            # msglist.append(i)
        msglist.append(stvol)


    # load_variable()
    if T_ENABLE is True:
    # if stimer.isrunning() is True:
        mins, secs = divmod(SEC_CD, 60)
        hours, mins = divmod(mins, 60)
        timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
        sst="sleep in : "+ timer
        # sst="sleep in : "+stimer.update()
        msglist.append(sst)
    msglist.append(local_ip)
    #msglist.append("test")
    msglist.append(NETSTAT)
    msglist.append(cputemp)

    status= status.replace("(0%)", "")
    status= status.replace("(volume", "\nvolume")

    # myoled.display(status, (0,0))

    #myoled.showmsg(status)

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

    global P_COUNT

#    print("P_COUNT = " + str(P_COUNT))
    for x in range(4):
        idx=(P_COUNT*4)+x
        if idx < totline:
            sm=str(msglist[idx])
            text += sm
            text +="\n"
        else:
            break

        # print(text)
    myoled.display(text, (0,0))
    text=""
    P_COUNT+=1
    if P_COUNT > (totpage-1):
        P_COUNT=0

old_station=""
old_vol=""
def anychange(status): #not used
    change = False
    if "playing" in status or "paused" in status:
        global old_station
        global old_vol
        #srink status
        inrep = status.index("repeat")-4
        status= status[:inrep]

        # crop station info
        inbrace =status.index("[")
        station = status[:inbrace]
        # print("station = " + station)
        # split limited length char to list

        # crop playing info
        indvol=status.index("volume")
        indel=status.index("/0")
        state=status[inbrace:indel]
        state=state.replace("#", " ")
        # split limited length char to list

        #crop volume info
        stvol=status[indvol+8:]

        # print("stvol"+stvol)
        if station!=old_station :
            change=True
            print ("station change")

        if stvol!=old_vol:
            change=True
            print ("volume change")
        # print("state = " + state)
        old_station=station
        old_vol=stvol
    return change

def getNetData():
        #required intall netstat
        global NETSTAT
        OUT = subprocess.check_output("netstat -e -n -i | grep wlan0  -A 10 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'", shell=True)
        #OUT = subprocess.check_output("ifconfig wlan0 | grep wlan0  -A 10 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'", shell=True)
        NETSTAT=str(OUT)
        sbr = NETSTAT.index("(")+1
        ebr = NETSTAT.index(")")
        NETSTAT = "RX = " + NETSTAT[sbr:ebr]
        NETSTAT= NETSTAT.replace('i','')

        # OUT = subprocess.check_output("iwconfig wlan0 | grep Quality |  awk '{print substr ($4$5, 7, 3)}'", shell=True)
        # dbm=b'\xff'
        dbm = subprocess.check_output("/usr/sbin/iwconfig wlan0 | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2", shell=True)
        # dbm = subprocess.check_output("/usr/sbin/iwconfig wlan0 | grep Signal | awk '{print $4}'", shell=True)
        # try:
        #     dbm = subprocess.check_output("iwconfig wlan0 | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2", shell=True)
        # except:
        #     dbm=b'\xff'
        #OUT = subprocess.check_output("ifconfig wlan0 | grep wlan0  -A 10 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'", shell=True)

        signal =  dbm.decode("utf-8")
        # signal=str(dbg)
        # if dbm:
            # dbm_num = int(dbm)
            # print("prcnt= "+ str(translate(dbm_num, -100,0,0,100)))
            # quality = 2 * (dbm_num + 100)
            # print("{0} dbm_num = {1}%".format(dbm_num, quality))
            # signal = str("sig = {1}%".format(dbm_num, quality))
        # sbr = signal.index("(")+1
        # ebr = signal.index("d")
        # dbtopercent(dbm)

        # NETSTAT = NETSTAT + " "+signal[5:]+ "dBm"
        NETSTAT = NETSTAT + dbtopercent(dbm) #+ signal[1:]
        # if dbm:
            # NETSTAT = NETSTAT + dbtopercent(dbm) #+ signal[1:]
        # try:
        #     NETSTAT = NETSTAT + dbtopercent(dbm) #+ signal[1:]
        # except:
        #     NETSTAT
def translate(value, leftMin, leftMax, rightMin, rightMax): #not used
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)


    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
def dbtopercent(value):
    # inval=0
    # try:
    #     inval=int(value)
    # except:
    #     inval =(-50)
    # percent = 100 x (1 – (PdBm_max – PdBm) / (PdBm_max – PdBm_min))

    inval=int(value)
    if inval != 0:
        percent = 100 * (1 - ((-1) - inval) / ((-1)- (-98)))
        pct=str(math.floor(percent))
        # pct=pct[:]
        # print("percent="+pct)
        return " sig: " +pct + "%"
    else:
        return " sig: 0%"

def send_wall_message(message: str):
    try:
        # Send the message using the 'wall' command
        subprocess.run(["wall"], input=message.encode(), check=True)
        print("Message sent to all logged-in users.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send message: {e}")


class sleeptimer:
    def startcdown(self, minutes):
        global T_ENABLE
        global SEC_CD
        T_ENABLE=True
        SEC_CD=minutes*60
        return
    # cancel sleep timer
    def stopcdown(self):
        global T_ENABLE
        global SEC_CD
        T_ENABLE=False
        SEC_CD=0
        print("sleep timer stopped by user")
        return

    def countdown(self):
        global T_ENABLE
        global SEC_CD
        #print("sec cd = "+str(SEC_CD))
        if T_ENABLE is True and PLAYING is True:
            mins, secs = divmod(SEC_CD, 60)
            timer = f'{mins:02d}:{secs:02d}'
            #print(f'Time left: {timer}', end='\r')
            SEC_CD -= 1
            # print("iradio_oled" +str(SEC_CD))
            if SEC_CD==0:
                print("\nTime's up!")
                os.system("mpc stop")
                send_wall_message("mpc stopped due sleep timer defined by user")
                T_ENABLE =False
                #quit()
    # auto stop reset counting
    def resetas(self):
        global ASSECCD
        print("auto stop timer resetted")
        ASSECCD =0
    #get auto stop second running
    def getsecac(self):
        global ASSECCD
        return str(ASSECCD)

    def autostop(self):
        global PLAYING
        global ASSECCD
        global ASCDOWN
        global ASSECMX
        if ASCDOWN is True and PLAYING is True:
            ASSECCD+=1
            # print("iradio_oled auto stop  "+str(ASSECCD))
            if ASSECCD ==ASSECMX:
                print("\nauto stop due a 1 hour no user activity!")
                send_wall_message("mpc stopped due 1 hour without user control")
                os.system("mpc stop")
            elif ASSECCD > (ASSECMX+1):
                ASSECCD=ASSECMX+1


    def loopy(self):
        # self.cekStart()
        # self.cekStop()
        self.countdown()
        self.autostop()
        # threading.Timer(1, loopy).start()  # Schedule the function to run again in 1 second

    def isrunning(self):
        global T_ENABLE
        return T_ENABLE


    def update(self):
        global T_ENABLE
        global SEC_CD
        #print("sec cd = "+str(SEC_CD))
        if T_ENABLE is True:
            mins, secs = divmod(SEC_CD, 60)
            hours, mins = divmod(mins, 60)
            timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
            return "sleep in > "+str(timer)
        else:
            return "off" # do not change

# def getUsage():
#     global NETSTAT
#     while True:
#         OUT = subprocess.check_output("netstat -e -n -i | grep wlan0  -A 5 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'", shell=True)
#         NETSTAT=str(OUT)
#
U_COUNT = 20
MAXUCOUNT = 25
STOP_COUNT = 0
SCREEN_SLEEP = False
def loop():
    global U_COUNT
    global MAXUCOUNT
    global STOP_COUNT
    global P_COUNT
    global SCREEN_SLEEP
    global systemReady
    global PLAYING
    global local_ip
    old_status=""
    status = ""
    # os.system("mpc > tmp")
    status = subprocess.check_output("mpc", shell=True).decode("utf-8")
    if "playing" in status or "paused" in status:
        PLAYING = True
    else:
        PLAYING = False
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
    if U_COUNT == 20:
        if "playing" in status or "paused" in status:
            # displaytooled2()
            displaytooled(status)
            # stimer.updateplayer(True)
            MAXUCOUNT=25
            STOP_COUNT=0
        else:
            # myoled.clear(1)
            # myoled.display("player stopped", (xpos,ypos))
            MAXUCOUNT = 20
            STOP_COUNT +=1
            # print("STOP_COUNT" + str(STOP_COUNT))
            if STOP_COUNT > 600:
                myoled.display("",(0,0))
                STOP_COUNT=201
                if SCREEN_SLEEP is False:
                    SCREEN_SLEEP = True
                    # myoled.clear(1)
            else:
                if STOP_COUNT == 2:
                    local_ip=local_ip.replace("IP: ","")
                secac=msleeptimer.getsecac()
                if secac==str(ASSECMX+1):
                    myoled.display("player stopped due\n1 hour no user\nactivity", (0,0))
                    os.system()
                else:
                    ypos = random.randint(0,30)
                    xpos = random.randint(0,50)
                    myoled.display("player stopped\n" +  local_ip, (xpos,ypos))
            #sleep(0.4)
    U_COUNT +=1
    if U_COUNT == 25:

        systemReady+=1
        if systemReady > 8:
            systemReady = 8
        getNetData()
        updateCPUtemp()
        #NETSTAT =  status.decode("utf-8")
    if U_COUNT > MAXUCOUNT:
        U_COUNT = 20

    old_status=status

    msleeptimer.loopy()

    # threading.Timer(1, loop).start()  # Schedule the function to run again in 1 second

msleeptimer=sleeptimer()

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
        self.timer_loop=looptimer(1, loop)
        self.timer_loop.start()
    def stop(self):
        self.timer_loop.stop()

class display:
    def resettimer(self):
        global U_COUNT
        U_COUNT = 15;
        print("reset timer")
        return
    def setPage(self,up):
        global P_COUNT
        global U_COUNT
        U_COUNT=19
        print(f'U_COUNT = {U_COUNT}')
        if up is True:
            P_COUNT+=1
        else:
            P_COUNT=0
        displaytooled(status)

    def delay(self, time):
        global U_COUNT
        if time > 0:
            U_COUNT = 0- time
        return

    def frezeeDisplay(self, delay):
        global U_COUNT
        U_COUNT = 20-delay;
        # print("reset timer for " + str(delay))
        return

    def display(self, msg, pos):
        myoled.display(msg, pos)
        return

    def displaybig(self, msg):
        myoled.displaybig(msg)
        return


    def displayfs(self, msg, fs):
        global P_COUNT
        myoled.displayfs(msg, fs)
        P_COUNT=0
        return

    def display(self, msg, rndom):
        mx=128-len(msg)*6
        print("mx="+str(mx))
        if mx<0:
            mx =0
        ypos = random.randint(0,54) if rndom else 0
        xpos =  random.randint(0,mx)if rndom else 0
        myoled.display(msg, (xpos,ypos))
        return


