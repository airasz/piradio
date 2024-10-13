#!/usr/bin/python

import os
import oledis
import textwrap
import subprocess
import random
import threading
from time import sleep
import mpc_sleep_timer

myoled= oledis.oled()
stimer=mpc_sleep_timer.mpctimer()
local_ip = ""
NETSTAT = ""
def getlocal_ip():
    global local_ip
    cmd= "hostname -I"
    result= subprocess.check_output(cmd, shell=True)
    local_ip =  result.decode("utf-8")
    if ":" in local_ip:
        local_ip=local_ip[:(local_ip.index(":")-4)]
        # local_ip=local_ip.rstrip
        # local_ip=local_ip.replace("\n", "")

    local_ip = "IP: " + local_ip
    print(local_ip)
# getlocal_ip()
P_COUNT=0
def displaytooled(status):
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
    if stimer.isrunning() is True:
        sst="sleep in : "+stimer.update()
        msglist.append(sst)
    msglist.append(local_ip)
    #msglist.append("test")
    msglist.append(NETSTAT)    

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


# def getUsage():
#     global NETSTAT
#     while True:
#         OUT = subprocess.check_output("netstat -e -n -i | grep wlan0  -A 5 | grep 'RX packets' |  tail -1 | awk '{print $6$7}'", shell=True)
#         NETSTAT=str(OUT)
#
U_COUNT = 0
MAXUCOUNT = 5
STOP_COUNT = 0
SCREEN_SLEEP = False
def loop():
    global U_COUNT
    global MAXUCOUNT
    global STOP_COUNT
    global P_COUNT
    global SCREEN_SLEEP
    old_status=""
    status = ""
    # os.system("mpc > tmp")
    status = subprocess.check_output("mpc", shell=True)
    status =  status.decode("utf-8")
    # print(status)
    # if status != old_status:
    # if anychange(status) is True:
    #     if SCREEN_SLEEP is True:
    #         print("wake up oled")
    #         SCREEN_SLEEP = False
    #         myoled.show()
    #     P_COUNT = 0
    #     U_COUNT= 0
    stimer.loopy()
    # print(stimer.update())
    # print("U_COUNT" + str(U_COUNT))
    if U_COUNT == 0:
        if "playing" in status or "paused" in status:
            displaytooled(status)
            MAXUCOUNT=5
            STOP_COUNT=0
        
        else:
            # myoled.clear(1)
            # myoled.display("player stopped", (xpos,ypos))
            MAXUCOUNT = 0
            STOP_COUNT +=1

            # print("STOP_COUNT" + str(STOP_COUNT))
            if STOP_COUNT > 10:
                myoled.display("",(0,0))
                STOP_COUNT=11
                if SCREEN_SLEEP is False:
                    SCREEN_SLEEP = True
                    # myoled.clear(1)
            else:
                ypos = random.randint(0,54)
                xpos = random.randint(0,50)
                myoled.display("player stopped", (xpos,ypos))
            #sleep(0.4)
    U_COUNT +=1
    if U_COUNT == 5:
        getNetData()
        #NETSTAT =  status.decode("utf-8")
    if U_COUNT > MAXUCOUNT:
        U_COUNT = 0

    old_status=status
    threading.Timer(1, loop).start()  # Schedule the function to run again in 1 second


loop()

class display:
    def resettimer(self, msg):
        U_COUNT = 1;
        print("reset timer")
        return

    def display(self, msg, pos):
        myoled.display(msg, pos)
        return

    def display(self, msg, rndom):
        mx=128-len(msg)*6
        ypos = random.randint(0,54) if rndom else 0
        xpos =  random.randint(0,mx)if rndom else 0
        myoled.display(msg, (xpos,ypos))
        return
