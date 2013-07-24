#!/usr/bin/env python3

import time
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import quick2wire.i2c as q2w_i2c
import twitalu_globals as globals

# Useful port expander registers
IODIRA = 0x00
IODIRB = 0x01
IPOLA = 0x02
IPOLB = 0x03
GPPUA = 0x0C
GPPUB = 0x0D
GPIOA = 0x12
GPIOB = 0x13

# Each of the following functions require these arguments:
#  port_expand_addr = {0x20, 0x21, 0x22} 	(hex address)
#  port				= {A, B}				(expander port)
#  value			= {0b00000000}			(8-bit data value)

# This function sets the port's pull up resistors
# For pull-up, value = 0b11111111. Port must be set to input.
def set_IO_PULL_UP(port_expand_addr, port, value):
	with q2w_i2c.I2CMaster() as bus:
		if port == 'A':			
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, GPPUA, value))
		elif port == 'B':
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, GPPUB, value))

# This function sets the port's logic polarity
# For inverting, value = 0b11111111. For non-inverting, value = 0b00000000
def set_IO_POL(port_expand_addr, port, value):
	with q2w_i2c.I2CMaster() as bus:
		if port == 'A':			
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, IPOLA, value))
		elif port == 'B':
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, IPOLB, value))

# This function sets the direction of a port's GPIO
# For input, value = 0b11111111. For output, value = 0b00000000
def set_IO_DIR(port_expand_addr, port, value):
	with q2w_i2c.I2CMaster() as bus:
		if port == 'A':			
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, IODIRA, value))
		elif port == 'B':
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, IODIRB, value))

# This function writes data to the port expander
def write_data(port_expand_addr, port, value):
	with q2w_i2c.I2CMaster() as bus:
		if port == 'A':			
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, GPIOA, value))
		elif port == 'B':
			bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, GPIOB, value))
			
# This function reads data from the port expander
def read_data(port_expand_addr, port):
	with q2w_i2c.I2CMaster() as bus:
		if port == 'A':
			return bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, GPIOA),
			q2w_i2c.reading(port_expand_addr, 1))[0][0]
		elif port == 'B':
			return bus.transaction(
			q2w_i2c.writing_bytes(port_expand_addr, GPIOB),
			q2w_i2c.reading(port_expand_addr, 1))[0][0]