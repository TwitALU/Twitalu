#!/usr/bin/env python3

# Notes:
# Register B data is on Port A of Port Expander B (0x21)
# Register B control is on Port B of Port Expander B
# Output Enable (OE) pins are ACIVE LOW

# Port Expander B:
# I2C address 0x21
#				Port B			Port A
#					   _________  
#	Inverted Buf OE 0[|	   B 	|]0 B0
#		Port Buf OE	1[|  		|]1 B1
#	  ADL in Buf OE 2[|   MCP	|]2 B2
#		  Reg B CLK 3[|	 23017	|]3 B3
#					4[| 		|]4 B4
#					5[|			|]5 B5
#					6[| 		|]6 B6
#					7[|_________|]7 B7

# Includes
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')
import twitalu_I2C as I2C

# Defines
port_expand_B_addr = 0x21

# This function initialises both ports of Port Expander B
def init():
	I2C.set_IO_DIR(port_expand_B_addr, 'A', 0x00) # set port as output
	I2C.write_data(port_expand_B_addr, 'A', 0x00) # write all zeros
	I2C.set_IO_DIR(port_expand_B_addr, 'B', 0x00) # set port as output
	I2C.write_data(port_expand_B_addr, 'B', 0b00000111) # disable all buffers, drive clock low
	clear_register()

# This function writes 8 bits to Port A
def write_port(data):
	I2C.write_data(port_expand_B_addr, 'A', data)

# This function clears Port A
def clear_port():
	I2C.write_data(port_expand_B_addr, 'A', 0x00) # write all zeros
	
# This function controls the buffer connected to the Port Expander (enable = 1, disable = 0)
def set_port_buffer(enable):
	old_value = I2C.read_data(port_expand_B_addr, 'B') # read in the previous control pins
	if enable == 1:
		mask = 0b11111101 # set port buffer signal low
		new_value = old_value & mask # AND
	elif enable == 0:
		mask = 0b00000111 # set port buffer signal high
		new_value = old_value | mask # OR
	I2C.write_data(port_expand_B_addr, 'B', new_value) # write to Port B
	
# This function controls the buffer connected to the inverted data (enable = 1, disable = 0)
def set_inverted_buffer(enable):
	old_value = I2C.read_data(port_expand_B_addr, 'B') # read in the previous control pins
	if enable == 1:
		mask = 0b11111110 # set inverted buffer signal low
		new_value = old_value & mask # AND
	elif enable == 0:
		mask = 0b00000111 # set inverted buffer signal high
		new_value = old_value | mask # OR
	I2C.write_data(port_expand_B_addr, 'B', new_value) # write to Port B
	
# This function controls the buffer connected to the ADL bus (enable = 1, disable = 0)
def set_ADL_buffer(enable):
	old_value = I2C.read_data(port_expand_B_addr, 'B') # read in the previous control pins
	if enable == 1:
		mask = 0b11111011 # set port buffer signal low
		new_value = old_value & mask # AND
	elif enable == 0:
		mask = 0b00000011 # set port buffer signal high
		new_value = old_value | mask # OR
	I2C.write_data(port_expand_B_addr, 'B', new_value) # write to Port B
	
# This function clocks in data to Reg B from the currently selected buffer
def clock_data():
	# drive clock high
	old_value = I2C.read_data(port_expand_B_addr, 'B') # read in the previous control pins
	clock_high_mask = 0b00001000
	clock_high_value = old_value | clock_high_mask # OR, set clock high
	I2C.write_data(port_expand_B_addr, 'B', clock_high_value)
	
	# drive clock low
	old_value = I2C.read_data(port_expand_B_addr, 'B') # read in the previous control pins
	clock_low_mask = 0b11110111
	clock_low_value = old_value & clock_low_mask # AND, set clock low
	I2C.write_data(port_expand_B_addr, 'B', clock_low_value)

# This function returns the 8 bits on Port A	
def read_register():
	return(I2C.read_data(port_expand_B_addr, 'A'))

# This function writes 8 bits to the Register
def write_register(data):
	write_port(data)
	set_port_buffer(1)
	clock_data()
	set_port_buffer(0)
	
# This function writes 8 inverted bits to the Register
def write_inverted_register(data):
	write_port(data)
	set_inverted_buffer(1)
	clock_data()
	set_inverted_buffer(0)
	
# This function writes 8 bits to the Register from the ADL bus
def write_ADL_register():
	set_ADL_buffer(1)
	clock_data()
	set_ADL_buffer(0)
	
# This function clears the Register
def clear_register():
	clear_port()
	set_port_buffer(1)
	clock_data()
	set_port_buffer(0)