from machine import Pin
from utime import sleep
import network as net
import urequests as ureq

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
    print(ssid)
    print(password)
    wlan = net.WLAN(net.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(wlan.status())
        
    while not wlan.isconnected():
        print('Waiting for connection...')
        print(wlan.status())
        if wlan.isconnected(): print("CONNECTED")
        led.off()
        sleep(0.5)
        led.on()
        sleep(0.5)
    print("Connected")
    led.on()
    sleep(0.2)
    led.off()
    sleep(0.2)
    led.on()
    
def google_ping():
    r = ureq.get("http://www.google.com")
    print(r.content)
    r.close()

def get_status():
    print(wlan.status())

def send(msg):
    print("done") 
