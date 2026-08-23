import RPi.GPIO as GPIO
import time


def relay_trigger(relay_int, on_off, debug=False):
    '''
    wire positive between A and C on relay
    A to power, C to device

    relay_int = 5, 6, 13, 16, 19, 20, 21, 26
    on_off = on OR off
    debug = True OR False, defaults to False
    '''

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    Relay = [5, 6, 13, 16, 19, 20, 21, 26]

    if debug:
        print("setup relays")
    for i in range(len(Relay)):
        GPIO.setup(Relay[i], GPIO.OUT)
        GPIO.output(Relay[i], GPIO.HIGH)

    if debug:
        print("checking relay_int")
    if relay_int in Relay:
        if debug:
            print("toggle relay")
        if on_off == "on":
            GPIO.output(relay_int, GPIO.LOW)
        elif on_off == "off":
            GPIO.output(relay_int, GPIO.HIGH)


for i in range(5):
    print("On for 5 seconds")
    relay_trigger(5, "on")
    time.sleep(5)
    print("Off for 5 seconds")
    relay_trigger(5, "off")
    time.sleep(5)
