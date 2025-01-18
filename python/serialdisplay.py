#!/usr/bin/python
import serial
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
stimer=mpcstimer.mpctimer()
local_ip = ""
NETSTAT = ""

cputemp=""

CDOWN = False
T_ENABLE= False
SEC_CD = 0
ON_MENU=False
ASCDOWN=True
ASSECCD=0
PLAYING= True
ASSECMX=3600
#setup connection
# con= serial.Serial()
# sport='/dev/ttyUSB0'


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
            # print(SEC_CD)
            if SEC_CD==0:
                print("\nTime's up!")
                os.system("mpc stop")
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
            # print("serial display auto stop  "+str(ASSECCD))
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
            return "off"


msleeptimer=sleeptimer()

sport=''
def cekport():
    global sport
    # output = result= subprocess.check_output("dmesg | grep tty", shell=True)
    tty =  subprocess.check_output("dmesg | grep tty", shell=True).decode("utf-8")
    if "ttyUSB" in tty:
       itty=tty.index("ttyUSB")
       sport = '/dev/'+tty[itty:(itty+7)]
       # sport = '/dev/ttyUSB0'
    else:
       sport = '/dev/ttyS1'
    print("usage serial port "+ sport[5:])

cekport()
con = serial.Serial(
    port=sport,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

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

def serialdisplay(msg):
    data= str.encode(msg)
    con.write(data)

def getlocal_ip():
    global local_ip
    cmd= "hostname -I | awk '{print$1}'"
    result= subprocess.check_output(cmd, shell=True)
    local_ip =  result.decode("utf-8")
    if ":" in local_ip:
        local_ip=local_ip[:(local_ip.index(":")-5)]
        # print("ipv6 exist")
        # print("length ip"+str(len(local_ip)))
        # local_ip=local_ip.rstrip
        # local_ip=local_ip.replace("\n", "")
    else:
        local_ip=local_ip[:len(local_ip)-1]
        # print("length ip"+str(len(local_ip)))
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

P_COUNT=0
def displaytooled_old(status):
    global local_ip
    global NETSTAT
    if len(local_ip) < 8:
        getlocal_ip()

    mlpl = 22# maximum length per line
    #srink status
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
    indel=status.index("/0")
    state=status[inbrace:indel]
    state=state.replace("#", " ")
    # split limited length char to list
    msglist=textwrap.wrap(state, mlpl)

    #crop volume info
    stvol=status[indvol:]

    # print("state = " + state)

    for i in infolist:
        msglist.append(i)

        # msglist.append(i)
    msglist.append(stvol)
    msglist.append(local_ip)
    #msglist.append("test")
    # msglist.append(NETSTAT)

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
    # for x in range(4):

    print(' '.join(msglist))
    # for x in msglist:
    #     # text+=str(msglist[x])
    #     sm=str(msglist[x])
    #     text += sm
    text=(' '.join(msglist))

    # for x in range(4):
    #     idx=(P_COUNT*4)+x
    #     if idx < totline:
    #         sm=str(msglist[idx])
    #         text += sm
    #         text +="\n"
    #     else:
    #         break

    print(text)
    # myoled.display(text, (0,0))
    # data= str.encode(text)
    # con.write(data)
    serialdisplay(text)
    text=""
    P_COUNT+=1
    if P_COUNT > (totpage-1):
        P_COUNT=0


def displaytooled(status):
    global local_ip
    global NETSTAT
    if len(local_ip) < 8:
        getlocal_ip()

    mlpl = 21# maximum length per line
    mlpp = 5 # maximum line per page
    #srink status
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
    msglist.append(local_ip)
    #msglist.append("test")
    msglist.append(NETSTAT)

    msglist.append(cputemp)
    status= status.replace("(0%)", "")
    status= status.replace("(volume", "\nvolume")

    # load_variable()
    if T_ENABLE is True:
    # if stimer.isrunning() is True:
        mins, secs = divmod(SEC_CD, 60)
        hours, mins = divmod(mins, 60)
        timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
        sst="sleep in : "+ timer
        # sst="sleep in : "+stimer.update()
        msglist.append(sst)
    # myoled.display(status, (0,0))

    #myoled.showmsg(status)
    msglist.append(sysinfo())
    totline=len(msglist)
    # print(totline)
    sm=""
    text=""
    totpage=int(len(msglist)/mlpp)
    ttlline=4*totpage
    if totline> ttlline:
        totpage+=1 #get actual page

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
        idx=(P_COUNT*mlpp)+x
        if idx < totline:
            sm=str(msglist[idx])
            text += sm
            text +="\n"
        else:
            break

    # print(text)
    # myoled.display(text, (0,0))
    # data= str.encode(text)
    # con.write(data)
    serialdisplay(text)
    text=""
    P_COUNT+=1
    if P_COUNT > (totpage-1):
        P_COUNT=0

old_station=""
old_vol=""
def anychange(status):
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
        NETSTAT=str(OUT)
        sbr = NETSTAT.index("(")+1
        ebr = NETSTAT.index(")")
        NETSTAT = "RX = " + NETSTAT[sbr:ebr]
        NETSTAT= NETSTAT.replace('i','')

        dbm = subprocess.check_output("/usr/sbin/iwconfig wlan0 | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2", shell=True)
        signal =  dbm.decode("utf-8")

        NETSTAT = NETSTAT + dbtopercent(dbm) #+ signal[1:]
def dbtopercent(value):
    inval=int(value)
    if inval != 0:
        percent = 100 * (1 - ((-1) - inval) / ((-1)- (-98)))
        pct=str(math.floor(percent))
        # pct=pct[:]
        # print("percent="+pct)
        return "\nWiFi signal: " +pct + "%"
    else:
        return "\nWiFi signal: 0%"
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
    global ON_MENU
    global PLAYING
    old_status=""
    status = ""
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
        status =  status.decode("utf-8")
        if "playing" in status or "paused" in status:
            PLAYING = True
        else:
            PLAYING = False
        if U_COUNT == 20:
            if "playing" in status or "paused" in status:
                # data= str.encode(status)
                # serialdisplay(status)
                displaytooled(status)
                MAXUCOUNT=25
                STOP_COUNT=0

            else:
                # myoled.clear(1)
                MAXUCOUNT = 20
                STOP_COUNT +=1

                # print("STOP_COUNT" + str(STOP_COUNT))
                if STOP_COUNT > 50:
                    # con.write("")
                    STOP_COUNT=51
                    if SCREEN_SLEEP is False:
                        SCREEN_SLEEP = True
                        # myoled.clear(1)
                else:
                    serialdisplay("player stopped")
                #sleep(0.4)
        U_COUNT +=1
        if U_COUNT == 25:
            getNetData()
            updateCPUtemp()
            #NETSTAT =  status.decode("utf-8")
        if U_COUNT > MAXUCOUNT:
            U_COUNT = 20

        old_status=status

    msleeptimer.loopy()
    # else:
    #     # status= "on menu"
    #     serialdisplay("on menu, press exit to reset")

    threading.Timer(1, loop).start()  # Schedule the function to run again in 1 second


loop()
#
class display:
    def resettimer(self, msg):
        global U_COUNT
        U_COUNT = 10;
        # print("reset timer")
        return

    def frezeeDisplay(self, delay):
        global U_COUNT
        U_COUNT = 20-delay;
        # print("reset timer for " + str(delay))
        return

    def display(self, msg, pos):
        # myoled.display(msg, pos)
        serialdisplay(msg)
        return

    def display(self, msg, rndom):
        mx=128-len(msg)*6
        ypos = random.randint(0,54) if rndom else 0
        xpos =  random.randint(0,mx)if rndom else 0
        # myoled.display(msg, (xpos,ypos))
        serialdisplay(msg)
        return

    def onmenu(self, onmenu):
        global ON_MENU
        ON_MENU=onmenu
        return

    def getmenu(self):
        global ON_MENU
        return ON_MENU
