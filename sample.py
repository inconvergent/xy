#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from xy.device import Device
from time import sleep


PENUP = 140
PENDOWN = 160
XMAX = 150
YMAX = 150
TTY = '/dev/ttyUSB0'



def main():

  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    device.penup()
    raw_input('enter to start ...')

    # device.home()
    device.move(XMAX,YMAX)
    device.move(0,0)

    device.penup()

    raw_input('\n\ndone ...')


if __name__ == '__main__':
  main()

