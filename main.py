from machine import Pin
from utime import sleep
import network as net

# use onboard LED which is controlled by Pin 25
# on a Pico W the onboad lLED is accessed differently,
# so commeent out the line below
# and uncomment the line below that
led = Pin("LED", Pin.OUT) # veresion for Pico
# led = Pin('LED', Pin.OUT) # version for Pico W

led.on()
sleep(0.5)
led.off()

# Turn the LED on
def on():
    print("ON")
    led.on()

# Turn the LED off
def off():
    print("OFF")
    led.off()

def wifi_connect(ssid, password):
    global wlan
    wlan = net.WLAN(net.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(wlan.status())
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)

def get_status():
    print(wlan.status())

def send(msg):
    print("done") 
