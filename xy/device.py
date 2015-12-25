# # -*- coding: utf-8 -*-

from __future__ import with_statement
from __future__ import print_function

import serial
from time import sleep

class Device(object):

  def __init__(self, port, penup, pendown):
    print('init ...')
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

    sleep(2)
    self.pen(self.__penup)
    print('started')

  def __enter__(self):
    # self.__init__(port)
    return self

  def __exit__(self,*arg, **args):
    print('closing ...')
    if self.serial:
      try:
        self.serial.close()
      except Exception as e:
        print(e)
        raise
    print('closed') 

  def __read(self):
    data = []
    # print('read')
    while True:
      # print('read ...')
      c = self.serial.read(1)
      # print(c)
      if c == '\n':
        return ''.join(data)
      data.append(c)
      # print('data', data)

  def __write(self, *args):
    print('write')
    self.serial.xonxoff = True
    line = ' '.join(map(str, args))
    print(line)
    self.serial.write('%s\r\n' % line)
    print(self.__read())
    # self.serial.xonxoff = False
    # print('done')

  def home(self):
    self.__write('G28')

  # def set_relative(self):
    # self.__write('G91')
  # def set_absolute(self):
    # self.__write('G90')

  def move(self, x, y):
    self.__x = x
    self.__y = y
    self.__write(
      'G1', 
      'X%s' % x,
      'Y%s' % y,
      'F800'
    )

  def rel_move(self, x, y):
    self.__x += x
    self.__y += y
    self.__write(
      'G1', 
      'X%s' % self.__x,
      'Y%s' % self.__y,
      'F800'
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

  def penup(self):
    self.pen(self.__penup)

  def pendown(self):
    self.pen(self.__pendown)

  def gcode(self, g):
    for line in g.lines:
      self.__write(line)

