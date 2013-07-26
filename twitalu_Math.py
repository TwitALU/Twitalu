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
	
# 16 bit subtraction
def Sub(num1, num2):
	result = 0
	
	if (num1 - num2) < 0: result -= 65536
	
	# Split the 16 bit input subtrahend into two 8 bit integers
	num2lo = extract_byte(num2, 'low')
	num2hi = extract_byte(num2, 'high')
	
	# Invert the subtrahend
	OP.CLC()
	RegB.write_inverted_register(num2lo)
	temp = OP.ADC(0)
	num2lo = OP.STA()
	RegB.write_inverted_register(num2hi)
	temp = OP.ADC(0)
	num2hi = OP.STA()
	
	# Reconstruct the subtrahend
	num2 = (num2hi << 8) + num2lo
	if globals.debug == True: print("Inverted: ", bin(num2))
	
	# Add 1 to the subtrahend to find the two's complement
	num2 = Add(num2, 1)
	if globals.debug == True: print("Incremented: ", bin(num2))
	
	# Correct for large numbers
	
	
	if globals.debug == True: print("Num1: ", num1, "Num2: ", num2)
	
	result += (Add(num1, num2)) & 0xFFFF
	
	return(result)
		
# 16 bit addition
def Add(num1, num2):
	# Split the two 16 bit input numbers into four 8 bit integers
	num1lo = extract_byte(num1, 'low')
	num1hi = extract_byte(num1, 'high')
	num2lo = extract_byte(num2, 'low')
	num2hi = extract_byte(num2, 'high')
	
	if globals.debug == True:
		print("num1lo: " , num1lo) 
		print("num1hi: " , num1hi << 8) 
		print("num2lo: " , num2lo) 
		print("num2hi: " , num2hi << 8) 
	
	# 6502 Assembly for 16 bit addition
	OP.CLC()			# clear the carry in
	OP.LDA(num1lo)
	cout = OP.ADC(num2lo)
	reslo = OP.STA()	# store sum of LSBs
	if globals.debug == True:
		print("cout1: " , cout)	
	ALU.set_C_IN(cout)
	OP.LDA(num1hi)
	OP.ADC(num2hi)		# add the MSBs using the carry from above
	reshi = OP.STA()	# store sum of MSBs
	cout = ALU.read_C_OUT()
	
	# Debug
	if globals.debug == True:
		print("cout: " , cout)
		print("reslo: " , reslo)
		print("reshi: " , reshi)
	
	# Return result
	return((cout << 16) + (reshi << 8) + reslo)
	
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