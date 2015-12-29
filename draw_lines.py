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



def main(args):

  from numpy import array
  from modules.utils import get_paths

  prefix = args.prefix
  scale = args.scale
  steps = args.steps
  stride = args.stride
  skip = args.skip

  paths = get_paths(prefix, XMAX, YMAX, skip, steps, stride, scale)
  
  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    device.do_paths(paths)


if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--prefix',
    type=str,
    required=True
  )
  parser.add_argument(
    '--steps',
    type=int,
    default=100000
  )
  parser.add_argument(
    '--stride',
    type=int,
    default=1
  )
  parser.add_argument(
    '--skip',
    type=int,
    default=0
  )
  parser.add_argument(
    '--scale',
    type=float,
    default=1.0
  )

  args = parser.parse_args()
  main(args)

