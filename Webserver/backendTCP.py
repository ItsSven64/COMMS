import socket as sock
import datetime

HOST    = "192.168.2.26"
PORT    = 65432

today = datetime.date.today()
filename = r"C:\Users\svend\Desktop\Programming\Python\SERVER" +r"\Logs -"+ str(today) + ".txt"
log = open(filename, "a")

def line_prepender(filename, line):
    #prepends the line to the file
    #arguments are self-explanatory
    #courtesy of eyquem on StackOverflow
    log.close()
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

'''
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
'''

while True:
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                print(data)
                data = data.decode() + "\n"
                line_prepender(filename, data)