#!usr/bin/env python
# import RPi.GPIO as GPIO
import time
import evdev

def get_ir_values():
    devices =[evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.name)  
        if(device.name == "sunxi-ir"):
            print("Using device",device.path,"\n")
            return device
        print("No device found!")

dev = get_ir_values()
time.sleep(1)
events = dev.read()

try:
    event_list = [event.value for event in events]
    print("Receved command:",event_list)
except BlockingIOError:
    print("No commands received. \n")
    
while True:
    event = dev.read_one()
    if event:
        print(event.value)