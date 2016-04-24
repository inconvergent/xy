#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from xy.device import Device


PENUP = 130
PENDOWN = 160

XMAX = 150
YMAX = 150
TTY = '/dev/ttyUSB0'



def main():

  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    for i in xrange(100000):
      if i % 2 == 0:
        print('down')
        device.pendown()
      else:
        print('up')
        device.penup()

      raw_input('flip ...')


    raw_input('\n\ndone ...')


if __name__ == '__main__':
  main()

