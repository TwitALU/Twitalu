#!/usr/bin/env python3

import time
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import twitalu_RegB as RegB
import twitalu_RegA as RegA
import twitalu_ALU as ALU
# This version of the math library requires no hardware to function.
# It returns the same variables as twitalu_Math.py

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
	
	
def Sub(num1, num2):
	return(num1 - num2)
		
def Add(num1, num2):
	return(num1 + num2)
	
def Div(num1, num2):
	return(num1 / num2)		
	
def Mult(num1, num2):
	return(num1 * num2)
	
def AND(num1, num2):
	return(num1 & num2)
	
def OR(num1, num2):
	return(num1 | num2)
	
def XOR(num1, num2):
	return(x ^ y)
	
def Shift_r(num1, num_bits):
	return(num1 >> num_bits)
	
def Shift_l(num1, num_bits):
	return(num1 << num_bits)