#!/usr/bin/python

try:
  from setuptools import setup, find_packages
except Exception:
  from distutils.core import setup, find_packages

packages = ['xy']

setup(
    name = 'xy',
    version = '0.0.1',
    author = '@fogleman, @inconvergent, ',
    install_requires = [
      'pyserial==2.7',
      'pyshp==1.2.3',
      'Shapely==1.5.13'
    ],
    license = '',
    packages = packages
)

