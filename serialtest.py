from serial import *

connected = False

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
while True:
    print(ser.read())
print("Stopping")