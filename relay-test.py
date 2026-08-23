import RPi.GPIO as GPIO
import time

# def relay_trigger(relay_int, low_high, duration, debug = False):
#     '''
#     wire positive between A and C on relay
#     A to power, C to device

#     relay_int = 5, 6, 13, 16, 19, 20, 21, 26
#     low_high = low OR high
#     time = time in action in ms
#     debug = True OR False, defaults to False
#     '''

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)

#     Relay = [5, 6, 13, 16, 19, 20, 21, 26]

#     if debug:
#         print("setup relays")
#     for i in range(len(Relay)):
#         GPIO.setup(Relay[i], GPIO.OUT)
#         GPIO.output(Relay[i], GPIO.HIGH)

#     if debug:
#         print("checking relay_int")
#     if relay_int in Relay:
#         if debug:
#             print("checking low_high")
#         if low_high == "low":
#             if debug:
#                 print("set relay to low")
#             GPIO.output(relay_int, GPIO.LOW)
#             time.sleep(duration)
#         elif low_high == "high":
#             if debug:
#                 print("set relay to high")
#             GPIO.output(relay_int, GPIO.HIGH)
#             time.sleep(duration)

#     if debug:
#         print("GPIO cleanup")
#     GPIO.cleanup()

def relay_toggle(relay_int, on_off, debug = False):
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

print("Manual trigger")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Relay = [5, 6, 13, 16, 19, 20, 21, 26]

for i in range(len(Relay)):
        GPIO.setup(Relay[i], GPIO.OUT)
        GPIO.output(Relay[i], GPIO.HIGH)

for i in range(5):
    key = input("Enter 1 to switch on, 0 to switch off and q to exit:\n")
    if key == "1":
        GPIO.output(5, GPIO.LOW)
    elif key == "0":
        GPIO.output(5, GPIO.HIGH)
    elif key == "q":
        GPIO.cleanup()
        break
    else:
        print("Please enter 1 or 0")

print(" Using toggle function")

for i in range(5):
    print("On for 5 seconds")
    relay_toggle(5, "on", debug = True)
    time.sleep(5)
    print("Off for 5 seconds")
    relay_toggle(5, "off", debug = True)
    time.sleep(5)