from serial import *

connected = False


while not connected:
    try:    
        #ser = Serial("COM4")
        
        #print(ser.read())
        continue
    except SerialException:
        continue
    else:        
        print("connect")
        connected = True

while True:
    #print(ser.read())
    break
print("Stopping")
