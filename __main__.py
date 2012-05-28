#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Jan Vlnas"
__version__ = "0.0.1"

import argparse
import brainx

parser = argparse.ArgumentParser(prog='pybrainx', description='BrainFuck interpreter with BrainLoller and BrainCopter support') #description=''
parser.add_argument('file', help='a file to process; text file for BrainFuck, PNG image for BrainLoller and BrainCopter')
parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
group = parser.add_mutually_exclusive_group()
group.add_argument('-l', '--brainloller', action='store_true', help='handle file as BrainLoller program (expects PNG image)')
group.add_argument('-c', '--braincopter', action='store_true', help='handle file as BrainCopter program (expects PNG image)')

args = parser.parse_args()


if args.brainloller:
    img = brainx.BrainLoller(args.file)
    data = img.load()
elif args.braincopter:
    img = brainx.BrainCopter(args.file)
    data = img.load
else:
    with open(args.file, encoding='ascii') as stream:
        data = stream.read()
program = brainx.BrainFuck(data, memory=b'\x00', output='', show_output=True)
program.run()
