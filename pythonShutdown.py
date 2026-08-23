#!/usr/bin/python3

# A Python shutdown and LED indicator script for Raspberry Pi using GPIO Zero.
#
# author:  Jon Witts
# license: GPL-3.0, see LICENSE included in this package

from gpiozero import Button, LED
from signal import pause
from time import sleep
from os import system

button = Button(23, hold_time=3)
led = LED(24)


def shutdown_pi():
    for i in range(3):
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
    system("sudo shutdown now -hP")


button.when_held = shutdown_pi
pause()
