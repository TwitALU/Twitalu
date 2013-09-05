#!/usr/bin/env python3

import time
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')
import quick2wire.i2c as q2w_i2c

# Arduino's i2c address
address = 0x10

# Arduino Reference:
#	switch (i2cData){
#	case 0x00:	clear display
#	case 0x01:	display add
#	case 0x02:	display sub			
#	case 0x03:	display mul			 
#	case 0x04:	display div			
#	case 0x05:	display sub			
#	case 0x06:	display mul		
#	case 0x07:	display div
#	case 0xF0:	display twitalu logo
#	case 0xF1:	display twitter logo

# This function writes a value into a register 
def write_register(addr, reg, data = 0x00):
	with q2w_i2c.I2CMaster() as bus:
		bus.transaction(
		q2w_i2c.writing_bytes(addr, reg, data))
	
def display_clear():
	write_register(address, 0x00)
	
def display_ADD():
	write_register(address, 0x01)
	
def display_SUB():
	write_register(address, 0x02)
	
def display_MUL():
	write_register(address, 0x03)
	
def display_DIV():
	write_register(address, 0x04)
	
def display_AND():
	write_register(address, 0x05)
	
def display_OR():
	write_register(address, 0x06)
	
def display_XOR():
	write_register(address, 0x07)
	
def display_ROR():
	write_register(address, 0x08)
	
def display_ROL():
	write_register(address, 0x09)
	
def display_twit_check():
	write_register(address, 0x0A)
	
def display_twit_send():
	write_register(address, 0x0B)
	
def display_wait():
	write_register(address, 0x0C)
	
def countdown(count):
	write_register(address, 0x0D, count)
	
def display_TEST():
	write_register(address, 0xF0)
	
def display_twitalu():
	write_register(address, 0xF1)
	
def emergency_stop():
	write_register(address, 0xFF)

