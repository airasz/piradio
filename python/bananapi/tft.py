#import module: install with 'easy_install -U pyserial'
import serial
from time import sleep

#Set end of file
eof = "\xff\xff\xff"

# eof = "ffffff"

#setup text for writing
txt = 'Hello wold'

#setup connection
con = serial.Serial(

    port='/dev/ttyS1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

while 1:
    #write text to Page 0 t0 txt variable(check the id of your text box) plus EOF
    # data=('page0.t1.txt='+txt+eof).encode()
    data= str.encode('page0.t1.txt='+txt)
    # data+=eof
    con.write(data)
    # con.write("test")
    print(data)
    # con.write(("page 0" + txt+ eof).encode())
    sleep(1)
