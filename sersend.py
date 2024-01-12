import serial

connected = False

while not connected:
    try:
        ser = serial("COM6")
    except:
        continue
    else:
        connected = True
        ser.timeout = 0.5

while True:
    ser.write(input("What do you want to send?").encode())
    ser.read_until("\x00")