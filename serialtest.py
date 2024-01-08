from serial import *

connected = False

def Handle_input(input, ser):
    match input:
        case 'start':
            print("STARTED")

while not connected:
    try:    
        print("sending start to COM6")
        ser = Serial("COM6")
        
        ser.write(b"start")
    except SerialException:
        continue
    else:        
        print("connect")
        ser.write(b"start")
        connected = True

print("Now reading")
input = ser.read_until(expected=b'\n')

