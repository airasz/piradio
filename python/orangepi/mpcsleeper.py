#!/usr/bin/env python3
import os.path
import os
import threading
import time
from time import sleep
import json

DATAFILE_='/home/timer.json'
CDOWN = False
T_ENABLE= False
SEC_CD = 0
S_VAL = 0
STARTRUNNING_ = False



def writeAfterStart():
    global CDOWN
    global SEC_CD
    global S_VAL
    global STARTRUNNING_
    global T_ENABLE
    jdata={"enable":T_ENABLE,
           "startrun":False,
           "svalue":0,
           "seconds":SEC_CD
        }
    with open(DATAFILE_, "w") as f:
        json.dump(jdata, f)

def load_variable():
    global CDOWN
    global SEC_CD
    global S_VAL
    global STARTRUNNING_
    global T_ENABLE
    try:
        with open(DATAFILE_, "r") as f:
            data = json.load(f)
            T_ENABLE = data.get("enable", False)
            STARTRUNNING_ = data.get("startrun", False)
            if STARTRUNNING_ is True:
                S_VAL = data.get("svalue", 120)
                SEC_CD = S_VAL
    except FileNotFoundError:
        pass
    if STARTRUNNING_ is True:
        writeAfterStart()

def startccdown(minutes):
    global CDOWN
    global SEC_CD
    global S_VAL
    global STARTRUNNING_
    global T_ENABLE
    CDOWN = True
    SEC_CD = minutes*60
    print("starting timer")
    return "starting timer"


def writeUpdate():
    global CDOWN
    global SEC_CD
    global S_VAL
    global STARTRUNNING_
    global T_ENABLE
    jdata={"enable":T_ENABLE,
           "startrun":STARTRUNNING_,
           "svalue":0,
           "seconds":SEC_CD
        }
    with open(DATAFILE_, "w") as f:
        json.dump(jdata, f)


def countingDown():
    global CDOWN
    global SEC_CD
    global S_VAL
    global STARTRUNNING_
    global T_ENABLE
    # print("sec cd = "+str(SEC_CD))
    load_variable()
	# if T_ENABLE is True:
 #        if STARTRUNNING_ is True:
 #
	# 	CDOWN = True
	# 	STARTRUNNING_=False

    if T_ENABLE is True:

        mins, secs = divmod(SEC_CD, 60)
        timer = f'{mins:02d}:{secs:02d}'
        #print(f'Time left: {timer}', end='\r')
        SEC_CD -= 1
        if SEC_CD%5==0:
            writeUpdate()
        #print(SEC_CD)
        if SEC_CD==0:
            print("\nTime's up!")
            os.system("mpc stop")
            CDOWN =False
            T_ENABLE=False
            writeUpdate()
            sleep(1)
            # quit()

    threading.Timer(1, countingDown).start()  # Schedule the function to run again in 1 second


countingDown()
print("starting timer")
