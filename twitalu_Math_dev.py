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
	numA = int(numA[2:])
	numB = int(numB[2:])
	operation = operation[2:]
	operation = operation.lower()
		
	# Decode operation and calculate
	if operation == "add":
		result = tMath.Add(numA, numB)
	elif operation == "sub":
		result = tMath.Sub(numA, numB)
	elif operation == "mul":
		result = tMath.Mult(numA, numB)
	elif operation == "div":
		result = tMath.Div(numA, numB)
		
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