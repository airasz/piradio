#!usr/bin/env python
import time
import serial


ser = serial.Serial(
  port='/dev/tty1',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=0.2 # timeout in reception in seconds
)

def serialReceive():
  received_data = ser.read() #read serial port
  data_left = ser.inWaiting() #check for remaining byte
  received_data += ser.read(data_left)
  # print (received_data)


i = 0
while True:
  EndCom = b'xffxffxff' #End of each command as bytes
  temp = 't0.txt="'+time.strftime('%H%M%S')+'"' #local time
  temp = temp.encode('ascii') #conversion unicode in ascii
  ser.write(temp + EndCom) #write in text field 'titre'
  print(temp + EndCom)
  i=i+1
  ser.write(b'n0.val=') #write value in numeric field 'n0'
  ser.write(str(i).encode('ascii'))
  ser.write(EndCom)
  serialReceive()
