#!/usr/bin/python
# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time

Relay = [5, 6, 13, 16, 19, 20, 21, 26]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("setup set to high")

for i in range(0,8):
    GPIO.setup(Relay[i], GPIO.OUT)
    GPIO.output(Relay[i], GPIO.HIGH)

print("enter try loop")
try:
    while True:
        print("set relays to low")
        for i in range(8):
            GPIO.output(Relay[i], GPIO.LOW)
            time.sleep(0.5)
        print("set relays to high")
        for i in range(8):
            GPIO.output(Relay[i], GPIO.HIGH)
            time.sleep(0.5)


except:
    GPIO.cleanup()


