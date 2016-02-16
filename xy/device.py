# -*- coding: utf-8 -*-

from __future__ import print_function

from serial import Serial
from time import sleep


class Device(object):

  def __init__(self, dev, penup, pendown, verbose=False):

    from serial import PARITY_NONE
    from serial import EIGHTBITS, STOPBITS_ONE
    from serial import STOPBITS_ONE

    self.serial = None

    self.verbose = verbose

    self.__penup = penup
    self.__pendown = pendown

    self.__x = 0.
    self.__y = 0.

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

    sleep(3)
    self.cmd('START')

    self.set_absolute()
    self.penup()

  def __enter__(self):
    return self

  def __exit__(self,*arg, **args):
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

  def home(self):
    self.__write('G28')

  def set_relative(self):
    self.__write('G91')

  def set_absolute(self):
    self.__write('G90')

  def move(self, x, y):
    self.__x = x
    self.__y = y
    self.__write(
      'G1',
      'X%s' % x,
      'Y%s' % y
    )

  def rel_move(self, x, y):
    self.__x += x
    self.__y += y
    self.__write(
      'G1',
      'X%s' % self.__x,
      'Y%s' % self.__y
    )

  def draw(self, points, up, down):
    if not points:
      return
    self.pen(up)
    self.move(*points[0])
    self.pen(down)
    for point in points:
      self.move(*point)
    self.pen(up)

  def pen(self, position):
    self.__write('M1', position)
    return

  def penup(self):
    self.pen(self.__penup)

  def pendown(self):
    self.pen(self.__pendown)

  def do_paths(self, paths):

    from time import time

    t0 = time()

    num = len(paths)

    print('total paths: {:d}'.format(num))
    raw_input('enter to start ...')

    for i, p in enumerate(paths):

      print('progress: {:d}/{:d} time: {:0.05f}'.format(i, num, time()-t0))

      self.move(*p[0,:])
      self.pendown()
      for xy in p[1:,:]:
        self.move(*xy)
      self.penup()

    self.penup()

    raw_input('enter to finish ... ')

