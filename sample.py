#!/usr/bin/python

from __future__ import print_function

from xy.device import Device
from time import sleep

PENUP = 100
PENDOWN = 5

XMAX = 300
YMAX = 300


TTY = '/dev/ttyUSB0'

def main():

  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:


    # raw_input('start ...')

    # device.write('M10')
    
    # device.write('M03 S50 P0')
    # device.move(0, 0)
    # device.move(5,5)
    # device.move(0,0)
    # device.pendown()
    # device.move(0,0)
    # device.move(0,0)

    raw_input('\n\ndone ...')

    # device.write('T1 0') #


if __name__ == '__main__':
  main()

