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
import twitalu_RegA as RegA
import twitalu_RegB as RegB
import twitalu_ALU as ALU
import twitalu_RegADD as RegADD

RegA.init()
RegB.init()
ALU.init()
RegADD.init()

delayTime = 0

def write_register(numA, numB):
	# Write Inputs
	RegA.write_register(numA)
	RegB.write_register(numB)

def input_test():
	# Get input numbers
	numA = int(input("Enter number A: "))
	numB = int(input("Enter number B: "))
	write_register(numA, numB)
	
def counter_test():
	numA = 1
	numB = 1
	
	while numB < 256:
		write_register(numA, numB)
		RegADD.clock_data()
		result = RegADD.read_register() + (ALU.read_C_OUT() << 8)
		print(numA, " +", numB, " = ", result)
		if result != (numA + numB):
			print("NumA: ", numA)
			print("Numb: ", numB)
			print("NumA: ", result)
			break
		numB += 1
		time.sleep(delayTime)
		

		

while True:
	ALU.unset_all()
	ALU.set_ADD(1)
	
	counter_test()
	
	# while True:
		# ALU.set_C_IN(1)
		# print("Carry Out: ", ALU.read_C_OUT())
		# time.sleep(delayTime)
		# ALU.set_C_IN(0)
		# print("Carry Out: ", ALU.read_C_OUT())
		# time.sleep(delayTime)
	

	break
	