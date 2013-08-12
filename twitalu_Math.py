#!/usr/bin/env python3

import time
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import twitalu_RegB as RegB
import twitalu_RegA as RegA
import twitalu_ALU as ALU
import twitalu_OPCODES as OP
import twitalu_globals as globals

def calculate(numA, operation, numB):
	# Remove defining characters, convert to int
	numA = int(numA)
	numB = int(numB)
	operation = operation
	operation = operation.lower()
		
	# Decode operation and calculate
	if operation == "+":
		result = Add(numA, numB)
	elif operation == "-":
		result = Sub(numA, numB)
	elif operation == "*":
		result = Mult(numA, numB)
	elif operation == "/":
		result = Div(numA, numB)
	elif operation == "AND":
		result = AND(numA, numB)
	elif operation == "OR":
		result = OR(numA, numB)
	elif operation == "XOR":
		result = XOR(numA, numB)
	elif operation == "ROR":
		result = Shift_r(numA, numB)
	elif operation == "ROL":
		result = Shift_l(numA, numB)
		
	# Return answer
	return(result)

# This function returns the upper or lower 8 bits from a 16 bit integer.
# 'high' = 15:8, 'low' = 7:0
def extract_byte(num, section):
	if section == 'high':
		mask = 0xFF00
		return((num & mask) >> 8)
	elif section == 'low':
		mask = 0x00FF
		return(num & mask)
	
# 8 bit subtraction
def Sub(num1, num2):
	result = 0
	
	if (num1 - num2) < 0: result -= 65536
	
	# Invert the subtrahend
	OP.CLC()
	RegB.write_inverted_register(num2)
	temp = OP.ADC(0)
	num2 = OP.STA()
	
	# Add 1 to the subtrahend to find the two's complement
	num2 = Add(num2, 1)
	
	result += (Add(num1, num2)) & 0xFFFF
	
	return(result)
		
# 8 bit addition
def Add(num1, num2):	
	# 6502 Assembly for 8 bit addition
	OP.CLC()			# clear the carry in
	OP.LDA(num1)		# load accumulator with num1
	cout = OP.ADC(num2)	# add num2 to accumulator
	result = OP.STA()	# store sum of num1 and num2

	# Return result
	return(result)
	
# Division 2
def Div(num1, num2):
	# Setup variables
	count = 0
	adder = num2
	
	# Insanity test
	if num2 == 0:
		return(0)
	
	# Repetadly increase num2, counting each time
	while adder <= num1:
		OP.CLC()
		adder = Add(adder, num2)
		count += 1
	
	return(count)		
	
# Multiplication
def Mult(num1, num2):
	result = 0
	if num2 > num1:
		num1 = num1 + num2
		num2 = num1 - num2
		num1 = num1 - num2
		# temp = num1
		# num1 = num2
		# num2 = temp
	for x in range(0, num2):
		result = Add(result, num1)
	return(result)
	
# 8 bit bitwise AND
def AND(num1, num2):
	OP.CLC()
	OP.LDA(num1)
	OP.AND(num2)
	result = OP.STA()
	return(result)
	
# 8 bit bitwise OR
def OR(num1, num2):
	OP.CLC()
	OP.LDA(num1)
	OP.ORA(num2)
	result = OP.STA()
	return(result)
	
# 8 bit bitwise XOR
def XOR(num1, num2):
	OP.CLC()
	OP.LDA(num1)
	OP.EOR(num2)
	result = OP.STA()
	return(result)
	
# Shift right by num_bits. Shifts zeros in from
# the left.
def Shift_r(num1, num_bits):
	if num_bits > 8: # limits the number of cycles
		num_bits = 8
	for x in range(0, num_bits):
		OP.LDA(num1)
		OP.LSR()
		num1 = OP.STA()
	return(num1)
	
# Rotate right by num_bits. C_IN specifies value of MSB.
def Rotate_r(num1, num_bits):
	if num_bits > 8: # limits the number of cycles
		num_bits = 8
	OP.SEC(num1 & 0b1)
	for x in range(0, num_bits):
		OP.LDA(num1)
		OP.ROR()
		num1 = OP.STA()
		OP.SEC(ALU.read_C_OUT())
	return(num1, ALU.read_C_OUT())
	
# shift l, rotate r, rotate l