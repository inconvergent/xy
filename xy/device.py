# # -*- coding: utf-8 -*-

from __future__ import with_statement
from __future__ import print_function

import serial
from time import sleep

class Device(object):

  def __init__(self, port, penup, pendown):
    self.serial = None

    self.__penup = penup
    self.__pendown = pendown

    self.__x = 0
    self.__y = 0

    self.serial = serial.Serial(
      port, 
      115200, 
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      # ser.timeout = 0.1 #1.5 to give the hardware handshake time to happen
      # xonxoff = False,
      # rtscts = False,
      # dsrdtr = False
    )

    sleep(0.5)
    self.write('START')

    self.set_absolute()
    self.penup()

  def __enter__(self):
    return self

  def __exit__(self,*arg, **args):
    if self.serial:
      try:
        self.write('STOP')
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
      # print('w',self.serial.inWaiting(), data)
      c = self.serial.read(1)
      if c == '\n':
        break
      data.append(c)

    return ''.join(data)

  def write(self, *args):
    self.__write(*args)

  def __write(self, *args):
    ow = self.serial.outWaiting()
    iw = self.serial.outWaiting()
    print('ow {:d} iw {:d}'.format(ow,iw))
    self.serial.xonxoff = True
    line = ' '.join(map(str, args))
    print(' < ' + line)
    self.serial.write('%s\r\n' % line)
    print(' > ' + self.__read())

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
      'Y%s' % y,
    )

  # def rel_move(self, x, y):
    # self.__x += x
    # self.__y += y
    # self.__write(
      # 'G1', 
      # 'X%s' % self.__x,
      # 'Y%s' % self.__y,
      # # 'F800'
    # )

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

  def gcode(self, g):
    for line in g.lines:
      self.__write(line)

