#!/usr/bin/env python3
import sys
import mpcstimer
import json

stimer=mpcstimer.mpctimer()


def get_sum_of_num(num1,num2,num3):
    return(int(num1)+int(num2)+int(num3))

def startstime(minutes):

    vval=int(minutes)*60
    print(vval)
    jdata={"enable":True,
           "startrun":True,
           "svalue":vval,
           "seconds":0
        }
    with open("/home/timer.json", "w") as f:
        json.dump(jdata, f)
    exit(0)



if __name__ == "__main__":
  minutes = sys.argv[1]
  startstime(minutes)

  # num2 = sys.argv[2]
  # num3 = sys.argv[3]
  # print(get_sum_of_num(num1, num2, num3))
