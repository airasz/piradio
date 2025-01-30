#!/usr/bin/python
import serial
import serial.tools.list_ports
import time


# Configure the serial connection
# Replace 'COM3' with your serial port (e.g., '/dev/ttyUSB0' on Linux)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
SERIAL_PORT="unset"
ENDER =b'\xFF\xFF\xFF'
def list_available_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def send_message(port, message):
    global available_ports
    global SERIAL_PORT
    """Send a message to the specified serial port if it's available."""
    # try:
    #     with serial.Serial(port, baudrate=115200, timeout=1) as ser:
    #         ser.write(message.encode('utf-8'))
    #         print(f"Message sent to {port}: {message}")
    # except serial.SerialException as e:
    #     print(f"Failed to send message to {port}: {e}")
    #     available_ports = list_available_ports()
    # message=message.replace("\n","\\r")
    if SERIAL_PORT == "unset":
        for i in available_ports:
            try:
                with serial.Serial(i, baudrate=115200, timeout=1) as ser:
                    ser.write(message)
                    # print(f"Message sent to {i}: {message}")
                    ser.close()
            except serial.SerialException as e:
                print(f"Failed to send message to {i}: {e}")
                available_ports = list_available_ports()
    else:
        try:
            with serial.Serial(port, baudrate=115200, timeout=1) as ser:
                ser.write(message)
                # print(f"Message sent to {port}: {message}")
        except serial.SerialException as e:
            print(f"Failed to send message to {port}: {e}")
            available_ports = list_available_ports()
# Example usage
available_ports = list_available_ports()
print("[Nextion] Available serial ports:", available_ports)


class display:
    def set_port(self, port):
        global SERIAL_PORT
        SERIAL_PORT= port
        return
    def send_command(self, cmd):
        global ENDER
        global SERIAL_PORT
        cmd=cmd.replace("\n","\\r")
        data=cmd.encode() + ENDER
        send_message(SERIAL_PORT, data)


# Allow some time for the connection to establish
# time.sleep(2)

def send_command(command):
    # Send the command to the Nextion display
    #data=(command + '\xFF\xFF\xFF').encode('utf-8') 
    #print("data: "+str(data))
    ender=b'\xFF\xFF\xFF'

    command=command.replace("\n","\\r")
    data=command.encode()
    ser.write((data+ender))  # Nextion commands end with three 0xFF
    #ser.write(b't1.txt="Hello, Nextion!"\xFF\xFF\xFF')  # Nextion commands end with three 0xFF

    # print(b't1.txt="Hello, Nextion!"\xFF\xFF\xFF')
    # ender=b'\xFF\xFF\xFF'
    # ser.write(command+ender)  # Nextion commands end with three 0xFF

    
    
    
# Example: Send a command to set the text of a text box
#send_command(b't1.txt="Hello, hai Nextion!"')  # Assuming 't0' is the ID of your text box
#send_command('t1.txt="Hello, Nextion! encode"')  # Assuming 't0' is the ID of your text box
# send_command('page page1')  # Assuming 't0' is the ID of your text box
# send_command('t1.txt="Hello, Nextion! encode"')  # Assuming 't0' is the ID of your text box

# # Close the serial connection
# ser.close()

