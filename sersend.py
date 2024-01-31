import serial
from time import sleep

connected = False

while not connected:
    try:
        print("connecting")
        ser = serial("COM9")
        sleep(0.5)
    except:
        continue
    else:
        connected = True
        print("connect")
        ser.timeout = 0.5

while True:
    print(ser.read())
    sleep(0.3)