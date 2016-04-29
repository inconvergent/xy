#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from xy.device import Device


PENUP = 130
PENDOWN = 160

SMAX = 150
TTY = '/dev/ttyUSB0'



def main(args):

  from modules.utils import get_paths_from_n_files as get

  pattern = args.pattern
  scale = args.scale
  scale_to_fit = args.scaleToFit
  steps = args.steps
  stride = args.stride
  skip = args.skip

  print(args)

  paths = get(pattern, SMAX, skip, steps, stride, scale, scale_to_fit)

  with Device(
    TTY,
    penup=PENUP,
    pendown=PENDOWN,
    verbose=False,
    min_delay=2000,
    max_delay=2000
  ) as device:

    device.do_paths(paths)


if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--pattern',
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

  parser.add_argument(
    '--scaleToFit',
    dest='scaleToFit',
    action='store_true'
  )
  parser.add_argument(
    '--no-scaleToFit',
    dest='scaleToFit',
    action='store_false'
  )
  parser.set_defaults(scaleToFit=False)

  args = parser.parse_args()
  main(args)

