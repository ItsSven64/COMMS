from serial import *

connected = False

command_char = '--'

def Handle_input(input, ser):
    match input:
        case 'start':
            print("STARTED")

def Handle_command(input):
    #ALL THE COMMANDS
    match input:
        case 'start':
            Check_communication()
            

def Check_communication():
    global ser
    connected = False
    while not connected:
        try:    
            print("sending start to COM6")
            ser = Serial(port="COM9", parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1)
            
        except SerialException:
            continue
        else:        
            print("connect")
            connected = True

if __name__ == '__main__':
    Check_communication()
    
    try:
        ser = Serial("COM9")
    except:
        pass

    while True:
        send = input("What do you want to send?")
        send = send.encode()
        ser.write(send)
        if send == 'stop':
            msg = 'wow\x00'
            msg.ljust(24, " ")
            ser.write(msg.encode())
        from_ti = ser.read_until(expected=b'\x00')
        from_ti = from_ti.decode()
        from_ti = from_ti.strip('\x00')
        print(from_ti)
        if from_ti.startswith(command_char): Handle_command(from_ti)

