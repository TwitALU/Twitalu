#!/usr/bin/env python3

# Notes:
# The ALU is controlled using Port Expander ALU (0x23)
# Data is not passed to the ALU through the Port Expander
# The ALU function signals (ORS, ANDS etc.) (OE) pins are ACIVE LOW

# Port Expander ALU:
# I2C address 0x23
# 				Port B			Port A
#					   _________  
#			   C_IN 0[|	  ALU	|]0 SUMS
#			  C_OUT 1[|  		|]1 ANDS
#	   OVERFLOW_OUT 2[|   MCP	|]2 ORS
#					3[|	 23017 	|]3 XORS
#					4[| 		|]4 SRS
#					5[|		 	|]5 
#					6[|		 	|]6 
#					7[|_________|]7 

# Includes
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')
import twitalu_I2C as I2C

# Defines
port_expand_ALU_addr = 0x23

# This function initialises both ports of Port Expander ALU, and resets the ALU
def init():
	I2C.set_IO_DIR(port_expand_ALU_addr, 'A', 0x00) # set Port A as output
	I2C.set_IO_DIR(port_expand_ALU_addr, 'B', 0b11111110) # set C_IN bit as output, C_OUT, OVERFLOW as input
	I2C.set_IO_POL(port_expand_ALU_addr, 'B', 0x00) # set to non-inverting logic
	reset_ALU()
	
def reset_ALU():
	I2C.write_data(port_expand_ALU_addr, 'A', 0xFF) # write all ones to Port A
	I2C.write_data(port_expand_ALU_addr, 'B', 0x00000000) # clear C_IN on Port B

# This function returns the carry out from the ALU
def read_C_OUT():
	test = 0b00000010 # carry out is set
	C_OUT = I2C.read_data(port_expand_ALU_addr, 'B') # C_OUT from ALU
	if (test & C_OUT) == 0b00000010: # test for carry out being 1
		return(1)
	elif (test & C_OUT) == 0b00000000: # test for carry out being 0
		return(0)

# This function returns the overflow flag from the ALU
def read_OVERFLOW_OUT():
	test = 0b00000100 # overflow out is set
	OVERFLOW_OUT = I2C.read_data(port_expand_ALU_addr, 'B') # OVERFLOW_OUT from ALU
	if (test & OVERFLOW_OUT) == 0b00000100: # test for carry out being 1
		return 1
	elif (test & OVERFLOW_OUT) == 0b00000000: # test for carry out being 0
		return 0
		
# This function sets the carry input to the ALU
def set_C_IN(C_IN):
	old_value = I2C.read_data(port_expand_ALU_addr, 'B') # read in the previous Port B
	if C_IN == 0:
		mask = 0b11111110
		new_value = old_value & mask # AND, unset
	elif C_IN == 1:
		mask = 0b00000001
		new_value = old_value | mask # OR, set	
	I2C.write_data(port_expand_ALU_addr, 'B', new_value)
	
# This function disables the output buffers of all
# the combinational logic blocks.
def unset_all():
	I2C.write_data(port_expand_ALU_addr, 'A', 0xFF) # write all ones to Port A
	
# This function passes the output of ADD to ALU_OUT
def set_ADD(enable):	
	old_control_bus = I2C.read_data(port_expand_ALU_addr, 'A') # read the previous Port A
	if enable == 1:
		mask = 0b11111110 # set ADD signal low
		new_control_bus = old_control_bus & mask # AND
	elif enable == 0:
		mask = 0b00011111 # set ADD signal high
		new_control_bus = old_control_bus | mask # OR
	I2C.write_data(port_expand_ALU_addr, 'A', new_control_bus) # activate SUM ouput

# This function passes the output of AND to ALU_OUT
def set_AND(enable):
	old_control_bus = I2C.read_data(port_expand_ALU_addr, 'A') # read the previous Port A
	if enable == 1:
		mask = 0b11111101 # set AND signal low
		new_control_bus = old_control_bus & mask # AND
	elif enable == 0:
		mask = 0b00011111 # set AND signal high
		new_control_bus = old_control_bus | mask # OR
	I2C.write_data(port_expand_ALU_addr, 'A', new_control_bus) # activate AND ouput

# This function passes the output of OR to ALU_OUT
def set_OR(enable):
	old_control_bus = I2C.read_data(port_expand_ALU_addr, 'A') # read the previous Port A
	if enable == 1:
		mask = 0b11111011 # set OR signal low
		new_control_bus = old_control_bus & mask # AND
	elif enable == 0:
		mask = 0b00011111 # set OR signal high
		new_control_bus = old_control_bus | mask # OR
	I2C.write_data(port_expand_ALU_addr, 'A', new_control_bus) # activate OR ouput

# This function passes the output of XOR to ALU_OUT
def set_XOR(enable):
	old_control_bus = I2C.read_data(port_expand_ALU_addr, 'A') # read the previous Port A
	if enable == 1:
		mask = 0b11110111 # set XOR signal low
		new_control_bus = old_control_bus & mask # AND
	elif enable == 0:
		mask = 0b00011111 # set XOR signal high
		new_control_bus = old_control_bus | mask # OR
	I2C.write_data(port_expand_ALU_addr, 'A', new_control_bus) # activate XOR ouput

# This function passes the output of Shift Right to ALU_OUT	
def set_SR(enable):
	old_control_bus = I2C.read_data(port_expand_ALU_addr, 'A') # read the previous Port A
	if enable == 1:
		mask = 0b11101111 # set SR signal low
		new_control_bus = old_control_bus & mask # AND
	elif enable == 0:
		mask = 0b00011111 # set SR signal high
		new_control_bus = old_control_bus | mask # OR
	I2C.write_data(port_expand_ALU_addr, 'A', new_control_bus) # activate Shift Right ouput