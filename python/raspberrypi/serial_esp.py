#!/usr/bin/python
import serial
from time import sleep

import textwrap
import subprocess
import random
import threading
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
       sport = '/dev/ttyS5'
    print("serial esp : usage serial port "+ sport[5:])

cekport()
con = serial.Serial(
    port=sport,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

def serialdisplay(msg):
    data= str.encode(msg)
    con.write(data)


class serialesp:
    def show(self, msg):
        serialdisplay(msg)
        return
