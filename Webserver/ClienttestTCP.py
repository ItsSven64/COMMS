import socket
import asyncio
from time import sleep

msgFromClient       = "Hello TCP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("162.168.2.26", 65432)
bufferSize          = 8192
closing_byte        = b'\x00'
req_msg             = b"/req"

print("These are the parameters:")
print("Address + Port {}".format(serverAddressPort))
print("Buffer size: " + str(bufferSize))
print("Closing byte: " + str(closing_byte))
print("Request byte: " + str(req_msg)) 

# Create a UDP socket at client side
TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCP_Socket.settimeout(1)
# Send to server using created UDP socket

async def recv_tcp():
    msg = ''
    while (msg != closing_byte):
        try:
            msgFromServer= await loop.run_in_executor(None, lambda: TCP_Socket.recv(bufferSize))
        except TimeoutError:
            break
        msg = "{}".format(msgFromServer[0])
        print(msg)

async def send_tcp():
        send = input("What do you want to send? ")
        match (send):
            case 'req log':
                #See COMMS SP for info
                try:
                    n_lines = int(input("How many lines? (0=*) "))
                    if (n_lines == 0):
                        print("Requesting entire log!")
                        data = 255
                    else:
                        data = 256-n_lines+1
                        #data = 256 - x
                        #x = 256 - data
                    TCP_Socket.sendall(req_msg, serverAddressPort) 
                    sleep(1)
                    TCP_Socket.sendall(data.to_bytes(1), serverAddressPort)  
                except ValueError:
                    print("Invalid input, please try again!")
                
                  

            case _: 
                TCP_Socket.sendall(str.encode(send), serverAddressPort)
         
        await asyncio.create_task(recv_tcp())     

async def main():
        tasks = [recv_tcp(), send_tcp()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    
    while(True):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())