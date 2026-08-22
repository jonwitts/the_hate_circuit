import RPi.GPIO as GPIO
import time

def relay_trigger(relay_int, low_high, duration, debug = False):
    '''
    relay_int = 5, 6, 13, 16, 19, 20, 21, 26
    low_high = low OR high
    time = time in action in ms
    debug = True OR False, defaults to False
    '''

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)

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
            print("checking low_high")
        if low_high == "low":
            if debug:
                print("set relay to low")
            GPIO.output(relay_int, GPIO.LOW)
            time.sleep(duration)
        elif low_high == "high":
            if debug:
                print("set relay to low")
            GPIO.output(relay_int, GPIO.HIGH)
            time.sleep(duration)

    if debug:
        print("GPIO cleanup")
    GPIO.cleanup()

relay_trigger(6, "low", 1, True)
#time.sleep(2)
relay_trigger(6, "high", 2, True)


#print("enter try loop")
#try:
#    while True:
#        print("set relays to low")
#        for i in range(len(Relay)):
#            GPIO.output(Relay[i], GPIO.LOW)
#            time.sleep(0.5)
#        print("set relays to high")
#        for i in range(len(Relay)):
#            GPIO.output(Relay[i], GPIO.HIGH)
#            time.sleep(0.5)


#except:
#    GPIO.cleanup()
