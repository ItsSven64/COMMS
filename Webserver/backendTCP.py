import os
import socket as sock
import datetime

HOST         = "localhost"
PORT         = 65432
closing_byte = b'--END OF FILE--'

today = datetime.date.today()
filename = r"C:\Users\svend\Desktop\Programming\Python\SERVER" +r"\Logs -"+ str(today) + ".txt"
log = open(filename, "a")
if os.stat(filename).st_size == 0:
    log.write("--END OF FILE--")

def line_prepender(filename, line):
    #prepends the line to the file
    #arguments are self-explanatory
    #courtesy of eyquem on StackOverflow
    log.close()
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def send_logs(conn, n_lines=0):
    #sends the logs file to the user
    #IP = target IP of client
    #n_lines = the number of lines that will be sent (counting from the bottom) (-1 = the entire file)
    global log
    print("sending logs!")
    log.close()
    log = open(filename, "r")
    print(n_lines)
    if (n_lines == 0):
        print("SEND ENTIRE LOG")
        while True:
            line = log.readline()
            conn.sendall(str.encode(line))
            if not line:
                break
    else:
        for i in range(n_lines):
            x = log.readline()
            conn.sendall(str.encode(x))
            if not x:
                break
    conn.sendall(b"\n")
    log.close()
    log = open(filename, "a")
    conn.sendall(b"--END OF FILE--")
    print("done!")


while True:
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}" + str(datetime.date.today()))
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
                if data == b'/req': 
                    data = conn.recv(1024)
                    print(data)
                    send_logs(conn, int.from_bytes(data, "little"))
                else:
                    data = data.decode() + "\n"
                    line_prepender(filename, data)
                    conn.send(b'Message received succesfully\n')