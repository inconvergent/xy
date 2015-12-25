#!/usr/bin/python

from __future__ import print_function

from xy.device import Device
from time import sleep


PENUP = 120
PENDOWN = 140
XMAX = 150
YMAX = 150
TTY = '/dev/ttyUSB0'


def make_path(p, vertices, edges, n=10):

  from dddUtils.ddd import order_edges

  e_order,v_ordered = order_edges(edges)
  xys = vertices[v_ordered,:]
  p.append(xys)

def get_paths(prefix, skip=0, steps=500, stride=1, scale=1):

  from dddUtils.ioOBJ import load_2d as load
  from glob import glob

  p = []

  for fn in sorted(glob(prefix + '*.2obj'))[skip:steps:stride]:
    print(fn)
    data = load(fn)
    vertices = data['vertices']
    vertices *= scale
    vertices[:,0] *= XMAX
    vertices[:,1] *= YMAX
    edges = data['edges']
    make_path(p, vertices, edges)

  return p

def do_paths(d, pp):

  for p in pp:
    d.move(*p[0,:])
    d.pendown()
    for xy in p[1:,:]:
      d.move(*xy)
    d.penup()

def main(args):

  from numpy import array

  prefix = args.prefix
  scale = args.scale
  steps = args.steps
  stride = args.stride
  skip = args.skip

  paths = get_paths(prefix, skip, steps, stride, scale)

  # print(paths)

  with Device(TTY, penup=PENUP, pendown=PENDOWN) as device:

    raw_input('start ...')
    do_paths(device, paths)
    # device.move(150,0)

    raw_input('done ...')

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

