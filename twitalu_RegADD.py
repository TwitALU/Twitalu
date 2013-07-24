#!/usr/bin/env python3

# Notes:
# The data output of the ALU is on Port A of Port Expander ADD (0x22)
# Adder Hold register control is on Port B of Port Expander ADD
# Output Enable (OE) pins are ACIVE LOW

# Port Expander ADD:
# I2C address 0x22
#				Port B			Port A
#					   _________ 
#	 ADD OUT Buf OE 0[|	  ADD	|]0 ADD0
#		 ADL Buf OE 1[|  		|]1 ADD1
#		Reg ADD CLK	2[|   MCP	|]2 ADD2
#					3[|	 23017 	|]3 ADD3
#					4[| 		|]4 ADD4
#					5[|			|]5 ADD5
#					6[| 		|]6 ADD6
#					7[|_________|]7 ADD7

# Includes
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')
import twitalu_I2C as I2C

# Defines
port_expand_ADD_addr = 0x22

# This function initialises both ports of Port Expander ADD
def init():
	I2C.set_IO_DIR(port_expand_ADD_addr, 'A', 0xFF) # set port A as input
	I2C.set_IO_POL(port_expand_ADD_addr, 'A', 0x00) # set port A logic to non-inverting
	I2C.set_IO_DIR(port_expand_ADD_addr, 'B', 0x00) # set port B as output
	I2C.write_data(port_expand_ADD_addr, 'B', 0b00000011) # disable both buffers, drive clock low
	
# This function clocks in the data from ADD_IN to the register
def clock_data():
	I2C.write_data(port_expand_ADD_addr, 'B', 0b00000111) # generate rising clock edge
	I2C.write_data(port_expand_ADD_addr, 'B', 0b00000011) # drive clock signal low
	
# This function returns the data bus on port A of Port Expander ADD, clock_data() must be called first
def read_register():
	I2C.write_data(port_expand_ADD_addr, 'B', 0b00000010) # enable ADD OUT buffer
	data = I2C.read_data(port_expand_ADD_addr, 'A')
	I2C.write_data(port_expand_ADD_addr, 'B', 0b00000011) # disable ADD OUT buffer
	return data
	
# This function passes the ADD_IN bus to the ADL bus, clock_data() must be called first
def set_ADL_bus(enable):
	if enable == 1:
		I2C.write_data(port_expand_ADD_addr, 'B', 0b00000001) # enable ADL buffer
	elif enable == 0:
		I2C.write_data(port_expand_ADD_addr, 'B', 0b00000011) # disable ADL buffer