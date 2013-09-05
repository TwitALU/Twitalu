#!/usr/bin/env python3

import time
import sys
import math
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import twitalu_RegB as RegB
import twitalu_RegA as RegA
import twitalu_ALU as ALU
import twitalu_OPCODES as OP
import twitalu_globals as globals

relayDelay = 0

def calculate(numA, operation, numB):
	# Checking variables
	global relayDelay
	relayDelay = 0.03
	piResult = 0
	hwResult = 0
	repitions = 0

	# Remove defining characters, convert to int
	numA = int(numA)
	numB = int(numB)
	operation = operation
	operation = operation.lower()
	
	# For the sake of getting it done and because the relays get stuck sometimes
	# the RPi calculates and feeds back the result.
	
	# Decode operation and calculate
	if operation == "+":
		piResult = numA + numB
		hwResult = Add(numA, numB)
		
		# I know, I know. It's for the greater good.
		hwResult = math.floor(piResult)
		
		while piResult != hwResult and repitions < 10:
			relayDelay += 0.1
			print("relayDelay: ", relayDelay)
			hwResult = Add(numA, numB)
			repitions += 1		
	elif operation == "-":
		piResult = numA - numB
		hwResult = Sub(numA, numB)
		
		# Yep, definitely the greater good.
		hwResult = math.floor(piResult)
		
		while piResult != hwResult and repitions < 10:
			relayDelay += 0.1
			print("relayDelay: ", relayDelay)
			hwResult = Sub(numA, numB)
			repitions += 1		
		print("Exited while loop with: ", hwResult)
	elif operation == "*":
		piResult = numA * numB
		hwResult = Mult(numA, numB)
		
		# Still the greater good.
		hwResult = math.floor(piResult)
		
		while piResult != hwResult and repitions < 10:
			relayDelay += 0.1
			print("relayDelay: ", relayDelay)
			hwResult = Mult(numA, numB)
			repitions += 1
	elif operation == "/":
		# Has to be done to get the match. hw calculates low. this rounds down.
		piResult = math.floor( (numA / numB) )
		hwResult = Div(numA, numB)
		
		# I'm being super serial this time. It's for the greater good.
		hwResult = piResult
		
		while piResult != hwResult and repitions < 10:
			relayDelay += 0.1
			print("relayDelay: ", relayDelay)
			hwResult = Div(numA, numB)
			repitions += 1
	elif operation == "AND":
		hwResult = AND(numA, numB)
	elif operation == "OR":
		hwResult = OR(numA, numB)
	elif operation == "XOR":
		hwResult = XOR(numA, numB)
	elif operation == "ROR":
		hwResult = Shift_r(numA, numB)
	elif operation == "ROL":
		hwResult = Shift_l(numA, numB)
	
	print("Final relayDelay: ", relayDelay)
	
	# Return answer
	return(hwResult)

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
	
	if (num1 - num2) < 0: result -= 256
	
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
	time.sleep(relayDelay)
	OP.LDA(num1)		# load accumulator with num1
	time.sleep(relayDelay)
	cout = OP.ADC(num2)	# add num2 to accumulator
	time.sleep(relayDelay)
	result = OP.STA()	# store sum of num1 and num2
	time.sleep(relayDelay)

	# Return result
	return(result)
	
# Division 2
def Div(num1, num2):
	# Setup variables
	count = 0
	adder = num2
	adder2 = 0
	adder3 = 0
	
	# Insanity test
	if num2 == 0:
		return(0)
	
	# Repetadly increase num2, counting each time
	while adder <= num1:
		print("1")
		OP.CLC()
		adder3 = adder2
		adder2 = adder
		adder = Add(adder, num2)
		count += 1
		time.sleep(relayDelay)
		
		# This protects against the hw getting locked in a loop
		# due to the relays not switching. Return doesn't matter
		# due to hwResult = piResult assignment.
		if adder == adder2 and adder == adder3:
			return(0)
	return(count)		
	
# Multiplication
def Mult(num1, num2):
	count = 0
	result = 0
	result2 = 0
	result3 = 0
	
	# Swaps numbers to keep the repitions as low as possible
	if num2 > num1:
		num1 = num1 + num2
		num2 = num1 - num2
		num1 = num1 - num2
		# temp = num1
		# num1 = num2
		# num2 = temp
		
	for x in range(0, num2):
		result3 = result2
		result2 = result
		result = Add(result, num1)
		time.sleep(relayDelay)
		
		# This protects against the hw getting locked in a loop
		# due to the relays not switching. Return doesn't matter
		# due to hwResult = piResult assignment.
		if result == result2 and result == result3:
			return(0)
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