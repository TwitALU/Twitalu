#!/usr/bin/env python3

import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import quick2wire.i2c as i2c
import nixie as nixie
import time

# The main parts of the program start here
with i2c.I2CMaster() as bus:
	
	print("-> Program Starting")
	nixie.init()
	time.sleep(1)
	nixie.module_info(1)
	
	nixie.tumble_display(1)
	time.sleep(1)
	
	nixie.write_value(int(input("Enter a number: ")), 1)
#	nixie.write_value(36802, 1)