import serial


data = "starting"


def main():
    s = serial.Serial(port="COM9", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
    s.flush()
    
    s.write("hii\x00".encode())
    mes = s.read_until('\x00').strip()
    print(mes.decode())


if __name__ == "__main__":
    main()