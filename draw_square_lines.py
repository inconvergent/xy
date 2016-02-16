#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from xy.device import Device


PENUP = 140
PENDOWN = 160
SMAX = 150
TTY = '/dev/ttyUSB0'

def lines(s, stp=0.0):

  from random import random
  from numpy import array

  x = 0
  num = 0

  res = []

  while x < s:
    x += random()*stp
    num += 1
    res.append(array([[x,0], [x,s]]))

  return res



def main(args=None):

  # fn = args.fn

  paths = lines(s=SMAX, stp=5.0)

  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    device.do_paths(paths)


if __name__ == '__main__':

  # import argparse

  # parser = argparse.ArgumentParser()
  # parser.add_argument(
    # '--fn',
    # type=str,
    # required=True
  # )

  # args = parser.parse_args()
  main()

