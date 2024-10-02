#!/usr/bin/python

import os
import oledis
import textwrap
import subprocess
import random
import threading

from time import sleep

myoled= oledis.oled()
localip = ""

def getlocalip():
    global localip
    cmd= "hostname -I"
    result= subprocess.check_output(cmd, shell=True)
    localip =  result.decode("utf-8")
    if ":" in localip:
        localip=localip[:(localip.index(":")-4)]

    localip = "IP: " + localip
    
getlocalip()

def displaytooled(status):
    global localip
    if len(localip) < 8:
        getlocalip()
    
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
    msglist.append(localip)


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
    for y in range(totpage):
        for x in range(4):
            idx=(y*4)+x
            if idx < totline:
                sm=str(msglist[idx])
                text += sm
                text +="\n"
            else:
                break

        # print(text)
        myoled.display(text, (0,0))
        text=""
        # if totpage > 1:
        #sleep(5)


#while True:
#    status = ""
#    os.system("mpc > tmp")
#    status = subprocess.check_output("mpc", shell=True)
#    status =  status.decode("utf-8")
#    if "playing" in status or "paused" in status:
#        displaytooled(status)
#    else:
#        ypos = random.randint(0,54)
#        xpos = random.randint(0,50)
#        myoled.display("player stopped", (xpos,ypos))
#        sleep(0.4)
U_COUNT = 0
def updateOled():
    global U_COUNT
    U_COUNT +=1
    status = ""
    os.system("mpc > tmp")
    status = subprocess.check_output("mpc", shell=True)
    status =  status.decode("utf-8")
    if U_COUNT > 5:
        if "playing" in status or "paused" in status:
            displaytooled(status)
        else:
            ypos = random.randint(0,54)
            xpos = random.randint(0,50)
            myoled.display("player stopped", (xpos,ypos))
            #sleep(0.4)
        U_COUNT = 0
    
    threading.Timer(1, updateOled).start()  # Schedule the function to run again in 1 second


updateOled()
