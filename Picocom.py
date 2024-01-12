import socket as sock
from serial import *
from time import sleep


msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
bufferSize          = 8192
closing_byte        = bytes([0])
req_msg             = 255

startMSG = b'+start'
stopMSG = b'+stop'

def Check_communication():
    global ser
    connected = False
    while not connected:
        try:    
            ser = Serial("COM6", 9600, timeout=0.2)
            
        except SerialException:
            continue
        else: 
            connected = True

def Get_info():
    global serverAddressPort
    global SSIDandPass
    
    done = False
    while not done:
        ser.write(b'+givecreds')
        from_ti = ser.read_until(expected=b'\x00')
        from_ti = from_ti.decode()
        creds = from_ti.split()
        if creds.length() > 4: done = False
        else:    
            serverAddressPort   = (creds[0], int(creds[1]))
            SSIDandPass         = (creds[2], creds[3])
            done = True

def recv_msg():
    ser.write(b'+start')
    msg = ser.read_until(b'\x00')
    return msg.decode()
    
def send_udp(msg):   
    TCP.sendto(startMSG, serverAddressPort)
    TCP.sendto(msg.encode(), serverAddressPort)
    TCP.sendto(stopMSG, serverAddressPort)

def recv_udp():
    msgFromServer = TCP.recvfrom(bufferSize)
    return msgFromServer.decode()
    
        
if __name__ == '__main__':
    blocked = False
    Check_communication()
    Get_info()
    TCP = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP.connect(("
    TCP.settimeout(0.2)
    
    while True:
        a = ser.read(7)
        if a.decode is '+start' and not blocked:
            blocked = True
            msg = recv_msg()
            if msg is not "":
                ser.write(b'+ack\x00')
                send_udp(msg)
                blocked = False
            else:
                ser.write(b'+fail\x00')
                blocked = False
                
        if a.decode is '+stop' and not blocked:
            #we missed something
            ser.write(b'+fail\x00')
            
        #check Server
        b = recv_UDP()
        if b is '+start' and not blocked:
            #read server input and store it into a buffer
            
            
        if b is '+stop' and blocked:
            #start writing the message to TI
        
        if b is '+stop' and not blocked:
            send_UDP("+fail")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
    
            
        
        
    
    
    
    
    
    


    
    

