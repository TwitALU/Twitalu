#!/usr/bin/env python3

import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import quick2wire.i2c as i2c
import time

# Here the address that the port expander is at is set
gateway_address = 0x04


# The following save the addresses of some of the registers in the port expander that we will need


# This function writes a value into a register 
def write_register(bus, addr, reg, b):
	bus.transaction(
	i2c.writing_bytes(addr, reg, b))

# This function reads a value from a register
def read_register(bus, addr, reg):
	return bus.transaction(
	i2c.writing_bytes(addr, reg),
	i2c.reading(addr, 1))[0][0]

# The main parts of the program start here
with i2c.I2CMaster() as bus:
	
	print("-> Program Starting")
	time.sleep(1)	
	
	while True:

		write_register(bus, gateway_address, 0x01, 0x02)
		time.sleep(0.5)
		write_register(bus, gateway_address, 0x01, 0x02)
		time.sleep(0.5)
