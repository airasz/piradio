#!/usr/bin/env python3
import os.path
import os
import threading
import time

CDOWN = False
SEC_CD = 0
T_RUNNING = False
ASCDOWN=True
ASSECCD=0
# def countingDown():
#     global CDOWN
#     global SEC_CD
#     print("sec cd = "+str(SEC_CD))
#     if CDOWN is True:
#         mins, secs = divmod(SEC_CD, 60)
#         timer = f'{mins:02d}:{secs:02d}'
#         #print(f'Time left: {timer}', end='\r')
#         SEC_CD -= 1
#         #print(SEC_CD)
#         if SEC_CD==0:
#             print("\nTime's up!")
#             os.system("mpc stop")
#             CDOWN =False
#             #quit()
#
#     threading.Timer(1, countingDown).start()  # Schedule the function to run again in 1 second
#
#
# countingDown()
#
# def startccdown(minutes):
#     global CDOWN
#     global SEC_CD
#     CDOWN = True
#     SEC_CD = minutes*60
#     print("starting timer")
#     return "starting timer"



class mpctimer:
    def cekStart(self):
        global CDOWN
        global startpath
        global SEC_CD
        if CDOWN is False:
            mstart = os.path.isfile(startpath)
            if mstart is True:
                CDOWN =True
                print("file exists\nsleep timer start")
                f = open(startpath, "r")
                val=f.read()
                tval=int(val)
                SEC_CD = tval
                print(SEC_CD)
                #os.remove(startpath)
    def startcdown(self, minutes):
        global CDOWN
        global SEC_CD
        CDOWN=True
        SEC_CD=minutes*60
        return

    def stopcdown(self):
        global CDOWN
        global SEC_CD
        CDOWN=False
        SEC_CD=0
        return

    def countdown(self):
        global CDOWN
        global SEC_CD
        #print("sec cd = "+str(SEC_CD))
        if CDOWN is True:
            mins, secs = divmod(SEC_CD, 60)
            timer = f'{mins:02d}:{secs:02d}'
            #print(f'Time left: {timer}', end='\r')
            SEC_CD -= 1
            #print(SEC_CD)
            if SEC_CD==0:
                print("\nTime's up!")
                os.system("mpc stop")
                CDOWN =False
                #quit()
    def resetas(self):
        global ASSECCD
        print("auto stop timer resetted")
        ASSECCD =0


    def autostop(self):
        global ASSECCD
        global ASCDOWN
        if ASCDOWN is True:
            ASSECCD+=1
            # print("ASSECCD "+str(ASSECCD))
            if ASSECCD ==3600:
                print("\nauto stop due a 1 hour no user activity!")
                os.system("mpc stop")
            elif ASSECCD > 3600:
                ASSECCD=3601


    def loopy(self):
        # self.cekStart()
        # self.cekStop()
        self.countdown()
        self.autostop()
        # threading.Timer(1, loopy).start()  # Schedule the function to run again in 1 second

    def isrunning(self):
        global CDOWN
        return CDOWN


    def update(self):
        global CDOWN
        global SEC_CD
        #print("sec cd = "+str(SEC_CD))
        if CDOWN is True:
            mins, secs = divmod(SEC_CD, 60)
            hours, mins = divmod(mins, 60)
            timer = f'{hours:02d}:{mins:02d}:{secs:02d}'

            return str(timer)
        else:
            return

#loop()
