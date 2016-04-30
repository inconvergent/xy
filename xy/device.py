# -*- coding: utf-8 -*-

from __future__ import print_function

from serial import Serial
from time import sleep


class Device(object):

  def __init__(
    self,
    dev,
    penup,
    pendown,
    min_delay=400,
    max_delay=1200,
    pen_delay=0.13,
    verbose=False
  ):

    from serial import PARITY_NONE
    from serial import EIGHTBITS
    from serial import STOPBITS_ONE

    self.serial = None

    self.verbose = verbose

    self.__min_delay = min_delay
    self.__max_delay = max_delay

    self.__penup = penup
    self.__pendown = pendown

    self.__x = 0.
    self.__y = 0.

    self.pen_delay = pen_delay

    self.serial = Serial(
      dev,
      115200,
      parity = PARITY_NONE,
      bytesize = EIGHTBITS,
      stopbits = STOPBITS_ONE,
      # timeout = 0.1,
      # xonxoff = True,
      # rtscts = False,
      # dsrdtr = False
    )

    self._moves = 0

    sleep(3)
    self.cmd('START')

    self.penup()

  def __enter__(self):

    raw_input('enter to start ...')

    return self

  def __exit__(self,*arg, **args):

    self.penup()
    raw_input('\n\ndone ...')

    if self.serial:
      try:
        self.cmd('STOP')
        self.serial.close()
      except Exception as e:
        print(e)
        raise

  # def __read(self):
    # data = []
    # res = ''
    # w = self.serial.inWaiting()
    # c = self.serial.read(w)
    # return c.strip()

  def __read(self):

    data = []
    while True:
      c = self.serial.read(1)
      if c == '\n':
        break
      data.append(c)

    return ''.join(data).strip()

  def cmd(self, *args):
    self.__write(*args)

  def __write(self, *args):

    ow = self.serial.outWaiting()
    iw = self.serial.inWaiting()
    self.serial.xonxoff = True


    line = ' '.join(map(str, args))
    if self.verbose:
      print(' o {:d} i {:d} < {:s}'.format(ow, iw, line))

    ow = self.serial.outWaiting()
    iw = self.serial.inWaiting()
    self.serial.write('%s\r\n' % line)

    r = self.__read()
    if self.verbose:
      print(' o {:d} i {:d} > {:s}'.format(ow, iw, r))

  def move(self, x, y, fast=False):
    self._moves += 1
    self.__x = x
    self.__y = y
    self.__write(
      'G1',
      'X%s' % x,
      'Y%s' % y,
      'L%s' % (self.__min_delay if fast else self.__max_delay),
      'U%s' % self.__max_delay
    )

  def pen(self, position):
    sleep(self.pen_delay)
    self.__write('M1', position)
    sleep(self.pen_delay)
    return

  def penup(self):
    self.pen(self.__penup)

  def pendown(self):
    self.pen(self.__pendown)

  def __get_total_moves(self, paths):
    num = len(paths)-1
    for p in paths:
      num += len(p)-1
    return num

  def do_dots(self, dots, info_leap=10):

    from time import time

    t0 = time()

    num = len(dots)

    print('# dots: {:d}'.format(num))

    self._moves = 0
    flip = 0

    for i, p in enumerate(dots):

      self.move(*p)
      self.pendown()
      self.penup()
      flip += 1
      if flip > info_leap:
        per = i/float(num)
        tot = (time()-t0)/3600.
        rem = tot/per - tot
        s = 'progress: {:d}/{:d} ({:3.03f}) run time: {:0.05f} hrs, remaining: {:0.05f} hrs'
        print(s.format(i, num, per, tot, rem))
        flip = 0
      flip += 1

    self.penup()

  def do_paths(self, paths, info_leap=10):

    from time import time

    t0 = time()

    num = len(paths)
    moves = self.__get_total_moves(paths)

    print('# paths: {:d}'.format(num))
    print('# moves: {:d}'.format(moves))

    self._moves = 0
    flip = 0

    for i, p in enumerate(paths):

      self.move(*p[0,:], fast=True)
      self.pendown()
      flip += 1
      for xy in p[1:,:]:
        self.move(*xy)
        if flip > info_leap:
          per = self._moves/float(moves)
          tot = (time()-t0)/3600.
          rem = tot/per - tot
          s = 'progress: {:d}/{:d} ({:3.03f}) run time: {:0.05f} hrs, remaining: {:0.05f} hrs'
          print(s.format(self._moves, moves, per, tot, rem))
          flip = 0
        flip += 1

      self.penup()

    self.penup()

