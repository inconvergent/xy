#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from xy.device import Device
from time import sleep

from numpy.random import random
from numpy import floor


PENUP = 140
PENDOWN = 160
XMAX = 150
YMAX = 150
TTY = '/dev/ttyUSB0'



def main():

  with Device(
    TTY,
    penup=PENUP,
    pendown=PENDOWN,
    verbose=True,
    min_delay=200,
    max_delay=1200
  ) as device:

    device.penup()
    device.move(floor(random()*XMAX),floor(random()*YMAX), fast=True)

    device.pendown()
    device.move(floor(random()*XMAX),floor(random()*YMAX), fast=False)
    device.penup()

    device.move(floor(random()*XMAX),floor(random()*YMAX), fast=True)

    device.pendown()
    device.move(floor(random()*XMAX),floor(random()*YMAX), fast=False)
    device.penup()

    device.move(0,0,fast=True)


if __name__ == '__main__':
  main()

