import socket
import asyncio
from time import sleep

msgFromClient       = "Hello TCP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("localhost", 65432)
startSize           = 4
bufferSize          = 1024
closing_byte        = b'--END OF FILE--'
req_msg             = b"/req"
closing_flag        = False

print("These are the parameters:")
print("Address + Port {}".format(serverAddressPort))
print("Buffer size: " + str(bufferSize))
print("Closing byte: " + str(closing_byte))
print("Request byte: " + str(req_msg)) 

# Create a UDP socket at client side
TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCP_Socket.connect(serverAddressPort)
TCP_Socket.settimeout(10)

print(TCP_Socket)
# Send to server using created UDP socket

async def recv_tcp(logs):
    msgFromServer = ''
    if logs:
        print("Log reading buffer")
        try:    
            while closing_byte.decode() not in msgFromServer:
                try:
                    msgFromServer= await loop.run_in_executor(None, lambda: TCP_Socket.recv(bufferSize))
                except TimeoutError:
                    break
                print(msgFromServer.splitlines())
        except TypeError:
            return
    else:
        print("Regularly reading buffer")
        try:
            msgFromServer= await loop.run_in_executor(None, lambda: TCP_Socket.recv(bufferSize))
        except TimeoutError:
                print("TIMEOUT, PLEASE TRY AGAIN LATER")
        print(msgFromServer.splitlines())

async def send_tcp():
        global closing_flag
        send = input("What do you want to send? ")
        match (send):
            case '/req log':
                #See COMMS SP for info
                try:
                    n_lines = int(input("How many lines? (0=*) "))
                    if (n_lines == 0):
                        print("Requesting entire log!")
                        data = 255
                    else:
                        data = n_lines
                    TCP_Socket.sendall(req_msg) 
                    sleep(1)
                    TCP_Socket.sendall(data.to_bytes(1))  
                    await asyncio.create_task(recv_tcp(True))
                except ValueError:
                    print("Invalid input, please try again!")                
            case '/close':
                closing_flag = True
                print("closing!")
                return
            case _: 
                TCP_Socket.sendall(str.encode(send))
                await asyncio.create_task(recv_tcp(False))
         
             

async def main():
        tasks = [recv_tcp(False), send_tcp()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    while not closing_flag:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    TCP_Socket.shutdown(socket.SHUT_RDWR)
    TCP_Socket.close()