#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Jan Vlnas"
__version__ = "0.0.0"

import argparse

parser = argparse.ArgumentParser(prog='pybrainx') #description=''
parser.add_argument('file', help='a file to process')
parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
group = parser.add_mutually_exclusive_group()
group.add_argument('-l', action='store_true', help='handle file as brainloller program')
group.add_argument('-c', action='store_true', help='handle file as braincopter program')

args = parser.parse_args()

print(args)