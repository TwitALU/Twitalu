#!/usr/bin/env python3

# Notes:
# Register A data is on Port A of Port Expander A (0x20)
# Register A control is on Port B of Port Expander A
# Output Enable (OE) pins are ACIVE LOW

# Port Expander A:
# I2C address 0x20
#				Port B			Port A
#					   _________  
#		Zero Buf OE 0[|	   A 	|]0 A0
#		Port Buf OE	1[|  		|]1 A1
#		Reg A CLK	2[|   MCP	|]2 A2
#					3[|	 23017 	|]3 A3
#					4[| 		|]4 A4
#					5[|			|]5 A5
#					6[| 		|]6 A6
#					7[|_________|]7 A7

# Includes
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')
import twitalu_I2C as I2C
import twitalu_globals as globals

# Defines
port_expand_A_addr = 0x20

# This function initialises both ports of Port Expander A
def init():
	I2C.set_IO_DIR(port_expand_A_addr, 'A', 0x00) # set port as output
	I2C.write_data(port_expand_A_addr, 'A', 0x00) # write all zeros
	I2C.set_IO_DIR(port_expand_A_addr, 'B', 0x00) # set port as output
	I2C.write_data(port_expand_A_addr, 'B', 0b00000011) # disable both buffers, drive clock low
	clear_register()

# This function writes 8 bits to Port A
def write_port(data):
	if globals.twitalu_v01_fixes == False:
		I2C.write_data(port_expand_A_addr, 'A', data)
	elif globals.twitalu_v01_fixes == True:
		# strip the incorrect bits
		bit0 = 0b00000001 & data
		bit1 = 0b00000010 & data
		bit2 = 0b00000100 & data
		bit3 = 0b00001000 & data
		
		# make copies of all bits
		bit0_copy = bit0
		bit1_copy = bit1
		bit2_copy = bit2
		bit3_copy = bit3
		
		# shift incorrect bits so they sit properly
		bit0 = bit1_copy >> 1
		bit1 = bit0_copy << 1
		bit2 = bit3_copy >> 1
		bit3 = bit2_copy << 1
		
		# reconstruct data
		data = data & 0xF0
		data = data | bit0
		data = data | bit1
		data = data | bit2
		data = data | bit3
		
		# write corrected data to port expander
		I2C.write_data(port_expand_A_addr, 'A', data)

# This function clears Port A
def clear_port():
	I2C.write_data(port_expand_A_addr, 'A', 0x00) # write all zeros
	
# This function controls the buffer connected to the Port Expander (enable = 1, disable = 0)
def set_port_buffer(enable):
	old_value = I2C.read_data(port_expand_A_addr, 'B') # read in the previous control pins
	if enable == 1:
		mask = 0b11111101 # set port buffer signal low
		new_value = old_value & mask # AND
	elif enable == 0:
		mask = 0b00000011 # set port buffer signal high
		new_value = old_value | mask # OR
	I2C.write_data(port_expand_A_addr, 'B', new_value) # write to Port B

# This function controls the output of the zero buffer (enable = 1, disable = 0)
def set_zero_buffer(enable):
	old_value = I2C.read_data(port_expand_A_addr, 'B') # read in the previous control pins
	if enable == 1:
		mask = 0b11111110 # set zero buffer signal low
		new_value = old_value & mask # AND
	elif enable == 0:
		mask = 0b00000011 # set zero buffer signal high
		new_value = old_value | mask # OR
	I2C.write_data(port_expand_A_addr, 'B', new_value) # write to Port B
	
# This function clocks in data to Reg A from the currently selected buffer
def clock_data():
	# drive clock high
	old_value = I2C.read_data(port_expand_A_addr, 'B') # read in the previous control pins
	clock_high_mask = 0b00000100
	clock_high_value = old_value | clock_high_mask # OR, set clock high
	I2C.write_data(port_expand_A_addr, 'B', clock_high_value)
	
	# drive clock low
	old_value = I2C.read_data(port_expand_A_addr, 'B') # read in the previous control pins
	clock_low_mask = 0b11111011
	clock_low_value = old_value & clock_low_mask # AND, set clock low
	I2C.write_data(port_expand_A_addr, 'B', clock_low_value)
	
# This function writes 8 bits to the Register
def write_register(data):
	write_port(data)
	set_port_buffer(1)
	clock_data()
	set_port_buffer(0)

# This function writes 8 zeros to the Register
def write_zero_register():
	set_zero_buffer(1)
	clock_data()
	set_zero_buffer(0)
	
# This function clears the Register
def clear_register():
	clear_port()
	set_port_buffer(1)
	clock_data()
	set_port_buffer(0)