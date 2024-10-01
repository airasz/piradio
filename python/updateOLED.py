#!/usr/bin/python

import os
import oledis
import textwrap
import subprocess
import random

from time import sleep

myoled= oledis.oled()
cmd= "hostname -I"
result= subprocess.check_output(cmd, shell=True)
localip =  result.decode("utf-8")

def displaytooled(status):
	#srink status
	inrep = status.index("repeat")
	status= status[:inrep]

	# crop station info
	inbrace =status.index("[")
	station = status[:inbrace]
	# print("station = " + station)
	# split limited length char to list
	infolist=textwrap.wrap(station, 25)

	# crop playing info
	indvol=status.index("volume")
	indel=status.index("/0")
	state=status[inbrace:indel]
	# split limited length char to list
	msglist=textwrap.wrap(state, 25)

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
		sleep(5)

while True:
	status = ""
	os.system("mpc > tmp")
	status = subprocess.check_output("mpc", shell=True)
	status =  status.decode("utf-8")
	if "playing" in status or "paused" in status:
		displaytooled(status)
	else:
		ypos = random.randint(0,54)
		xpos = random.randint(0,50)
		myoled.display("player stopped", (xpos,ypos))
		sleep(0.4)

