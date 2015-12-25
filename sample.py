#!/usr/bin/python

from __future__ import print_function

from xy.device import Device
from time import sleep

PENUP = 120
PENDOWN = 140

XMAX = 150
YMAX = 150


TTY = '/dev/ttyUSB0'

def main():

  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    raw_input('start ...')
    device.move(150,0)

    raw_input('done ...')


if __name__ == '__main__':
  main()

