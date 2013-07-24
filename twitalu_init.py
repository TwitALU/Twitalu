#!/usr/bin/env python3

import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import twitalu_I2C as I2C
import twitalu_RegA as RegA
import twitalu_RegB as RegB
import twitalu_RegADD as RegADD
import twitalu_ALU as ALU
import twitalu_globals as globals
import twitalu_Math as tMath

def init():
	# Initialise everything
	RegA.init()
	RegB.init()
	RegADD.init()
	ALU.init()
	globals.init()
	
while True:
	init()
	break
	