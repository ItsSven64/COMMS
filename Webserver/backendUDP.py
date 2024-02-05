import socket
import datetime


localIP     = '192.168.2.26'
localPort   = 25565
bufferSize  = 1024

msgFromServer       = "ACK, thank you for communicating!"
bytesToSend         = str.encode(msgFromServer)


closing_byte = bytes([255])
req_msg             = 255

today = datetime.date.today()
filename = r"C:\Users\svend\Desktop\Programming\Python\SERVER" +r"\Logs -"+ str(today) + ".txt"
log = open(filename, "a")

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

def line_prepender(filename, line):
    #prepends the line to the file
    #arguments are self-explanatory
    #courtesy of eyquem on StackOverflow
    log.close()
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def send_logs(IP, n_lines=0):
    #sends the logs file to the user
    #IP = target IP of client
    #n_lines = the number of lines that will be sent (counting from the bottom) (-1 = the entire file)
    global log
    print("sending logs!")
    log.close()
    log = open(filename, "r")
    if (n_lines == 0):
        while True:
            line = log.readline()
            UDPServerSocket.sendto(str.encode(line), IP)
            if not line:
                break
    else:
        for i in range(n_lines):
            x = log.readline()
            UDPServerSocket.sendto(str.encode(x), IP)
            if not x:
                break
    UDPServerSocket.sendto(closing_byte, IP)
    log.close()
    log = open(filename, "a")
    print("done!")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "{}".format(message)
    clientIP  = "{}".format(address)
    print(clientMsg)
    print(clientIP)
    print(int.from_bytes(message, byteorder='little'))
    match (message):
        case (b'\xff'):    
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            if (bytesAddressPair[0] == req_msg.to_bytes(1)): send_logs(address)
            else:   send_logs(address, 256-int.from_bytes(bytesAddressPair[0]))
            # Sending a reply to client
            continue
        case ("SHUTDOWN"):
            break
        case _:
            UDPServerSocket.sendto(message, address)
            line_prepender(filename, clientIP+ clientMsg + "@ " + str(datetime.datetime.now().strftime("%d-%m, %H:%M"))+'\n')


