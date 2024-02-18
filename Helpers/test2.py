from COMMS.Helpers.serrecv import Talker

t = Talker()





while True:
    t.send(input("? "))
    print(t.receive())
