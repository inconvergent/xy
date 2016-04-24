#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from xy.device import Device


PENUP = 130
PENDOWN = 160

SMAX = 150
TTY = '/dev/ttyUSB0'



def main(args):

  from modules.utils import get_paths_from_file as get

  fn = args.fn
  paths = get(fn, SMAX, spatial_concat = True)
  # from dddUtils.svg import export_svg
  # export_svg('fractures1.svg', paths, 1)


  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    device.do_paths(paths)


if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--fn',
    type=str,
    required=True
  )

  args = parser.parse_args()
  main(args)

