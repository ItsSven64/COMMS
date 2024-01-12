import socket
import network
import select
import sys
from time import sleep


msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
bufferSize          = 8192
closing_byte        = bytes([0])
req_msg             = 255

startMSG = b'+start\x00'
stopMSG = b'+stop\x00'

def Check_communication():
    
    global ser
    connected = False
    poll_obj = select.poll()
    poll_obj.register(sys.stdin, select.POLLIN)
    
    while not connected:
        poll_results = poll_obj.poll(0.2)
        
        if poll_results:
            data = sys.stdin.readline('\x00').strip()
            sys.stdout.write("received data: " + data + "\x00")
            
        else: sleep(0.5)
        

def Get_info():
    global serverAddressPort
    global SSIDandPass
    
    done = False
    while not done:
        ser.write(b'+givecreds\x00')
        from_ti = ser.read_until(expected=b'\x00')
        from_ti = from_ti.decode()
        creds = from_ti.split()
        if creds.length() > 4: done = False
        else:    
            serverAddressPort   = (creds[0], int(creds[1]))
            SSIDandPass         = (creds[2], creds[3])
            done = True

def recv_msg():
    ser.write(b'+start\x00')
    msg = ser.read_until(b'\x00')
    return msg.decode()
    
def send_udp(msg):   
    TCP.sendto(startMSG, serverAddressPort)
    TCP.sendto(msg.encode(), serverAddressPort)
    TCP.sendto(stopMSG, serverAddressPort)

def recv_udp():
    msgFromServer = TCP.recv(bufferSize)
    return msgFromServer.decode()
    
def connect_wifi():
    global wlan
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSIDandPass[0], SSIDandPass[1])
    trytime = 0
    while not wlan.isconnected():
        wlan.active(True)
        Get_info()
        wlan.connect(SSIDandPass[0], SSIDandPass[1])
        while wlan.isconnected() == False or trytime > 5:
            sleep(0.1)
            trytime += 0.1
        wlan.active(False)
    return wlan.ifconfig()[0]
        
if __name__ == '__main__':
    blocked = False
    Check_communication()
    
    host = socket.gethostname()
    TCP = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP.connect((serverAddressPort))
    TCP.settimeout(0.2)
    TCP.sendall(b'+init')
    
    #connect to wifi
    ser.write(b'connecting to wifi\x00')
    ip = connect_wifi()
    
    
    while True:
        a = ser.read(7)
        if a.decode == '+start' and not blocked:
            blocked = True
            msg = recv_msg()
            if msg != "":
                ser.write(b'+ack\x00')
                send_udp(msg)
                blocked = False
            else:
                ser.write(b'+fail\x00')
                blocked = False
                
        if a.decode == '+stop' and not blocked:
            #we missed something
            ser.write(b'+fail\x00')
            
        #check Server
        b = recv_UDP()
        if b == '+start' and not blocked:
            #read server input and store it into a buffer
            pass
            
            
        if b == '+stop' and blocked:
            #start writing the message to TI
            pass
        
        if b == '+stop' and not blocked:
            send_UDP("+fail")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
    
            
        
        
    
    
    
    
    
    


    
    

