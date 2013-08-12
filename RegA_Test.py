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
import time
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')
import twitalu_I2C as I2C
import twitalu_RegA as RegA

RegA.init()
while True:
	delayTime = 0.05
	RegA.write_register(0b00000001)
	time.sleep(delayTime)
	RegA.write_register(0b00000010)
	time.sleep(delayTime)
	RegA.write_register(0b00000100)
	time.sleep(delayTime)
	RegA.write_register(0b00001000)
	time.sleep(delayTime)
	RegA.write_register(0b00010000)
	time.sleep(delayTime)
	RegA.write_register(0b00100000)
	time.sleep(delayTime)
	RegA.write_register(0b01000000)
	time.sleep(delayTime)
	RegA.write_register(0b10000000)
	time.sleep(delayTime)