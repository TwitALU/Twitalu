#!/usr/bin/env python3

import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import quick2wire.i2c as i2c
import time

# Here the address that the port expander is at is set
address = 0x20
# The following save the addresses of some of the registers in the port expander that we will need
iodira_register = 0x00
iodirb_register = 0x01
gpioa_register = 0x12
gpiob_register = 0x13

# This function writes a value into a register 
def write_register(bus, reg, b):
	bus.transaction(
	i2c.writing_bytes(address, reg, b))

# This function reads a value from a register
def read_register(bus, reg):
	return bus.transaction(
	i2c.writing_bytes(address, reg),
	i2c.reading(address, 1))[0][0]

# The main parts of the program start here
with i2c.I2CMaster() as bus:
	# This line sets the direction of portA to outputs for the LEDs
	write_register(bus, iodira_register, 0x00)
	
	print("config done.")
	time.sleep(2)

	# While true will loop the contained code forever
	while True:
		# First turn on allthe LEDs
		write_register(bus, gpioa_register, 0b11111111)
		time.sleep(0.5)

		# ...then turn them off again0b
		write_register(bus, gpioa_register, 0b00000000)
		time.sleep(0.5)
