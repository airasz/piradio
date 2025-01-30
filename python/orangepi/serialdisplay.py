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

#
# sport=''
# def cekport():
#     global sport
#     # output = result= subprocess.check_output("dmesg | grep tty", shell=True)
#     tty =  subprocess.check_output("dmesg | grep tty", shell=True).decode("utf-8")
#     if "ttyUSB" in tty:
#        itty=tty.index("ttyUSB")
#        sport = '/dev/'+tty[itty:(itty+7)]
#        # sport = '/dev/ttyUSB0'
#     else:
#        sport = '/dev/ttyS1'
#     print("usage serial port "+ sport[5:])
#
# cekport()
# con = serial.Serial(
#     port=sport,
#     baudrate=115200,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
# )
#
# def serialdisplay(msg):
#     data= str.encode(msg)
#     con.write(data)

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


def list_available_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def send_message(port, message):
    global available_ports
    """Send a message to the specified serial port if it's available."""
    # try:
    #     with serial.Serial(port, baudrate=115200, timeout=1) as ser:
    #         ser.write(message.encode('utf-8'))
    #         print(f"Message sent to {port}: {message}")
    # except serial.SerialException as e:
    #     print(f"Failed to send message to {port}: {e}")
    #     available_ports = list_available_ports()

    for i in available_ports:
        try:
            with serial.Serial(i, baudrate=115200, timeout=1) as ser:
                ser.write(message.encode('utf-8'))
                # print(f"Message sent to {i}: {message}")
        except serial.SerialException as e:
            print(f"Failed to send message to {i}: {e}")
            available_ports = list_available_ports()

# Example usage
available_ports = list_available_ports()
print("Available serial ports:", available_ports)

if available_ports:
    port_to_use = available_ports[0]  # Use the first available port
    message_to_send = "Hello, Serial Port!"
    send_message(port_to_use, message_to_send)
else:
    print("No available serial ports found.")

P_COUNT=0

old_station=""
old_vol=""
U_COUNT = 20
MAXUCOUNT = 25
STOP_COUNT = 0
SCREEN_SLEEP = False
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
        # serialdisplay(msg)
        send_message(port_to_use, msg)
        return

    def display(self, msg, rndom):
        mx=128-len(msg)*6
        ypos = random.randint(0,54) if rndom else 0
        xpos =  random.randint(0,mx)if rndom else 0
        # myoled.display(msg, (xpos,ypos))
        # serialdisplay(msg)
        send_message(port_to_use, msg)
        return

    def onmenu(self, onmenu):
        global ON_MENU
        ON_MENU=onmenu
        return

    def getmenu(self):
        global ON_MENU
        return ON_MENU
