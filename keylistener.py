#!/usr/bin/python
# -*- coding: utf-8 -*-
import keyboard
import os
from time import sleep

VOLUME_UP = 115
VOLUME_DOWN = 114
NEXT = 163
PREV = 165
PLAY = 164
STOP = 166
SWITCH_PLAYLIST = False
MUTE = 113
B_MUTE = False
SP = 240
P_VOL = 0
C_VOL = 0

def getVol():
    status = "radio volume: 50%"
    os.system("mpc status > tmp")
    status =  open('tmp', 'r').read()
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
        os.system("mpc volume 0")
    else:
        os.system("mpc volume "+ str(C_VOL))
    
def getPlayState():
    status = "radio volume: 50%"
    os.system("mpc > tmp")
    status =  open('tmp', 'r').read()
    # volpos = status.index('playing')
    if 'playing' in status:
        return True
    else:
        return False

def setVOL(up):
    if (getPlayState()) is True:
        if up is True:
            print("set volume up")
            os.system("mpc volume +5")
        else:
            os.system("mpc volume -5")
        
def setSTATION(next):
    if (getPlayState()) is True:
        if next is True:
            os.system("mpc next")
        else:
            os.system("mpc prev")

def switchPLAYLIST():
    global SWITCH_PLAYLIST
    SWITCH_PLAYLIST = not SWITCH_PLAYLIST
    if SWITCH_PLAYLIST is True:
        os.system("mpc clear")
        sleep(0.1)
        os.system("mpc load koplo")
    else:
        os.system("mpc clear")
        sleep(0.1)
        os.system("mpc load radio")
        
while True:
    ev = keyboard.read_event()
    print(ev.scan_code)
    
    if ev.scan_code == VOLUME_UP and ev.event_type == keyboard.KEY_DOWN:
        setVOL(True)
    if ev.scan_code == VOLUME_DOWN and ev.event_type == keyboard.KEY_DOWN:
        setVOL(False)
    if ev.scan_code == NEXT and ev.event_type == keyboard.KEY_DOWN:
        setSTATION(True)
    if ev.scan_code == PREV and ev.event_type == keyboard.KEY_DOWN:
        setSTATION(False)
    if ev.scan_code == PLAY and ev.event_type == keyboard.KEY_DOWN:
        os.system("mpc play")
    if ev.scan_code == STOP and ev.event_type == keyboard.KEY_DOWN:
        os.system("mpc stop")
    if ev.scan_code == MUTE and ev.event_type == keyboard.KEY_DOWN:
        mute()
    if ev.scan_code == SP and ev.event_type == keyboard.KEY_DOWN:
        switchPLAYLIST()
    