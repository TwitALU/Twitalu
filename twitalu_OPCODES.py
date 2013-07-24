#!/usr/bin/env python3

import time
import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import twitalu_globals as globals

import twitalu_ALU as ALU
import twitalu_RegA as RegA
import twitalu_RegB as RegB
import twitalu_RegADD as RegADD

# OPCODES TO IMPLEMENT
# Addition
# CLC, LDA, ADC, STA
# Subtraction
# SEC, SBC
# Division
# LDY, BCC, INY, BNE

# This function returns the contents of the Accumulator.
def STA(): # STore Accumulator
	return(RegB.read_register())

# This function clears the Carry Flag
def CLC(): # CLear Carry
	ALU.set_C_IN(0)
	
# This function sets the Carry Flag
def SEC(): # SEt Carry
	ALU.set_C_IN(1)
	
# This function loads an 8-bit number into the Accumulator
# (Register B). Immidediate addressing only.
def LDA(num): # LoaD Accumulator
	RegB.write_register(num)

# This function loads a number into Register Y
def LDY(num): # LoaD Y register
	globals.Y = num
	
# This function loads a number into Register X
def LDX(num): # LoaD X register
	globals.X = num
	
# This function increments Register Y
def INY(): # INcrement Y
	globals.Y += 1
	
# This function increments Register X
def INX(): # INcrement X
	globals.X += 1
	
# This function decrements Register Y
def DEY(): # DEcrement Y
	globals.Y -= 1
	
# This function returns the value in Register Y
def STY(): # STore Y register
	return(globals.Y)

# This function stores the Accumulator in Register Y
def TAY(): # Transfer A to Y
	globals.Y = RegB.read_register()
	
# This function stores the Accumulator in Register X
def TAX(): # Transfer A to X
	globals.X = RegB.read_register()

# This function stores Register Y in the Accumulator
def TYA(): # Transfer Y to A
	RegB.write_register(globals.Y)

# This function stores Register X in the Accumulator
def TXA(): # Transfer X to A
	RegB.write_register(globals.X)

# This function returns True if carry flag is clear
def BCC(): # Branch on Carry Clear
	carry = ALU.read_C_OUT()
	if carry == 0:
		return(True)
	else:
		return(False)

# This function performs a logical shift right by one position.
def LSR(): # Logical Shift Right
	# Move accumulator val to Reg A
	RegA.write_register(STA())
	
	# Clear the carry, so we shift in zeros
	CLC()
	
	# Activate AND output
	ALU.unset_all()
	ALU.set_SR(1)
	
	# Read result
	RegADD.clock_data()
	SR = RegADD.read_register()
	
	# Store result in Accumulator
	LDA(SR)

# This function rotates an 8-bit number right one place, with
# the highest bit being set to the value of carry in and carry
# out gets set to the the lowest bit.
def ROR(): # ROtate Right
	# Move accumulator val to Reg A
	RegA.write_register(STA())
	
	# Activate AND output
	ALU.unset_all()
	ALU.set_SR(1)
	
	# Read result
	RegADD.clock_data()
	ROR = RegADD.read_register()
	
	# Store result in Accumulator
	LDA(ROR)
		
# This function performs the bitwise OR of the supplied
# 8-bit number and the number in the accumulator.
# Immediate addressing only.
def ORA(num): # bitwise OR with Accumulator
	# Write to register A
	RegA.write_register(num)
	
	# Activate OR output
	ALU.unset_all()
	ALU.set_OR(1)
	
	# Read result
	RegADD.clock_data()
	OR = RegADD.read_register()
	
	# Store result in Accumulator
	LDA(OR)
	
# This functions performs the bitwise XOR of the supplied
# 8-bit number and the number in the accumulator.
# Immediate addressing only.
def EOR(num): # bitwise Exclusive OR
	# Write to register A
	RegA.write_register(num)
	
	# Activate EOR output
	ALU.unset_all()
	ALU.set_XOR(1)
	
	# Read result
	RegADD.clock_data()
	EOR = RegADD.read_register()
	
	# Store result in Accumulator
	LDA(EOR)
	
# This functions performs the bitwise AND of the supplied
# 8-bit number and the number in the accumulator.
# Immediate addressing only.
def AND(num): # bitwise AND with accumulator
	# Write to register A
	RegA.write_register(num)
	
	# Activate AND output
	ALU.unset_all()
	ALU.set_AND(1)
	
	# Read result
	C_OUT = ALU.read_C_OUT()
	RegADD.clock_data()
	AND = RegADD.read_register()
	
	# Store result in Accumulator
	LDA(AND)

	return(C_OUT)
	
# This function adds an 8-bit number to the Accumulator.
# Immidediate addressing only.
def ADC(addend): # ADd with Carry
	# Write to register A
	RegA.write_register(addend)
	
	# Activate Adder Output
	ALU.unset_all()
	ALU.set_ADD(1)
	
	# Read result
	C_OUT = ALU.read_C_OUT()
	RegADD.clock_data()
	SUM = RegADD.read_register()
	
	# Store result in Accumulator
	LDA(SUM)
	
	return(C_OUT)

# This function subtracts an 8-bit number from the Accumulator.
# Immediate addressing only.
def SBC(subtrahend): # SuBtract with Carry
	# Locally store Accumulator
	minuend = STA()
	
	# Invert the subtrahend
	# RegB.write_inverted_register(subtrahend)	
	RegB.write_inverted_register(subtrahend)
	
	# Add 1 to the inverted subtrahend. Result is 2's complement
	ADC(1)
	twos_comp = STA()
	
	# Add the result of step 2 to the minuend
	LDA(minuend)
	ADC(twos_comp)
	
	C_OUT = ALU.read_C_OUT()
	
	return(C_OUT)	