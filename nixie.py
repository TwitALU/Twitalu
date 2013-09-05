#!/usr/bin/env python3

import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import quick2wire.i2c as q2w_i2c
import time
import math
import random

# Here the address blocks for the tube displays
# Adder hold register display
d1_m1 = 0x08
d1_m2 = 0x09
d1_m3 = 0x0a
d1_m4 = 0x0b
d1_m5 = 0x0c

# Register A display
d2_m1 = 0x2B
d2_m2 = 0x2C
d2_m3 = 0x2D
d2_m4 = 0x2E
d2_m5 = 0x2F

#Register B display
d3_m1 = 0x30
d3_m2 = 0x31
d3_m3 = 0x32
d3_m4 = 0x33
d3_m5 = 0x35

# The following save the addresses of some of the registers in the port expander that we will need
char_reg = 0x00 #[rw] 
addr_pins = 0x00 #[rd] read the address pins
bitmaph_reg = 0x01 #[rw]
bitmapl_reg = 0x02 #[rw]
sevenseg_reg = 0x03 #[rw]
dimmer_reg = 0x0B #[rw]
delay_reg = 0x0C #[rw]
command_reg = 0x0D #[rw]
fw_core = 0x0E #[rd]
fw_rev = 0x0F #[rd]

def init():
	blank_display()
	dim_display(0x75)

# This function writes a value into a register 
# This is an internal functions and should not be used outside of this file
def write_data(addr, reg, b):
	with q2w_i2c.I2CMaster() as bus:
		bus.transaction(
		q2w_i2c.writing_bytes(addr, reg, b))

# This function reads a value from a register
# This is an internal functions and should not be used outside of this file
def read_data(addr, reg):
	with q2w_i2c.I2CMaster() as bus:
		return bus.transaction(
		q2w_i2c.writing_bytes(addr, reg),
		q2w_i2c.reading(addr, 1))[0][0]
		
# Used for setting the brightness level of the displays
def dim_display(level, disp = 0):
	if(int(level) <= 0):
		new_lev = 0
	elif(int(level) >= 100):
		new_lev = 100
	else:
		new_lev = int(level)

	if(disp == 1):
		write_data(d1_m1, dimmer_reg, new_lev)	
		write_data(d1_m1, dimmer_reg, new_lev)
		write_data(d1_m3, dimmer_reg, new_lev)
		write_data(d1_m4, dimmer_reg, new_lev)
		write_data(d1_m5, dimmer_reg, new_lev)	

	elif(disp == 2):
		write_data(d2_m1, dimmer_reg, new_lev)
		write_data(d2_m2, dimmer_reg, new_lev)
		write_data(d2_m3, dimmer_reg, new_lev)
		write_data(d2_m4, dimmer_reg, new_lev)
		write_data(d2_m5, dimmer_reg, new_lev)
			
	elif(disp == 3):
		write_data(d3_m1, dimmer_reg, new_lev)
		write_data(d3_m2, dimmer_reg, new_lev)
		write_data(d3_m3, dimmer_reg, new_lev)
		write_data(d3_m4, dimmer_reg, new_lev)
		write_data(d3_m5, dimmer_reg, new_lev)
	
	else:
		# Dim them all
		dim_display(level, 1)
		dim_display(level, 2)
		dim_display(level, 3)
	
# Used for turning the displays off
def blank_display(disp = 0):
	if(disp == 1):
		# Make sure the burn in routine is stopped as it overrides the blank
		write_data(d1_m1, command_reg, 0x02)
		write_data(d1_m2, command_reg, 0x02)
		write_data(d1_m3, command_reg, 0x02)
		write_data(d1_m4, command_reg, 0x02)
		write_data(d1_m5, command_reg, 0x02)
		# Begin blanking the displays
		write_data(d1_m1, char_reg, 0b00010000)
		write_data(d1_m5, char_reg, 0b00010000)
		time.sleep(0.05)
		write_data(d1_m2, char_reg, 0b00010000)
		write_data(d1_m4, char_reg, 0b00010000)
		time.sleep(0.05)
		write_data(d1_m3, char_reg, 0b00010000)
		
	elif(disp == 2):
		# Disbale the burn in routine as it overrides blanking command
		write_data(d2_m1, command_reg, 0x02)
		write_data(d2_m2, command_reg, 0x02)
		write_data(d2_m3, command_reg, 0x02)
		write_data(d2_m4, command_reg, 0x02)
		write_data(d2_m5, command_reg, 0x02)
		# Beging blanking displays
		write_data(d2_m1, char_reg, 0b00010000)
		write_data(d2_m5, char_reg, 0b00010000)
		time.sleep(0.05)
		write_data(d2_m2, char_reg, 0b00010000)
		write_data(d2_m4, char_reg, 0b00010000)
		time.sleep(0.05)
		write_data(d2_m3, char_reg, 0b00010000)
		
	elif(disp == 3):
		# Disable the burn in routine as it overrides the blanking command
		write_data(d3_m1, command_reg, 0x02)
		write_data(d3_m2, command_reg, 0x02)
		write_data(d3_m3, command_reg, 0x02)
		write_data(d3_m4, command_reg, 0x02)
		write_data(d3_m5, command_reg, 0x02)
		# Begin blanking the displays
		write_data(d3_m1, char_reg, 0b00010000)
		write_data(d3_m5, char_reg, 0b00010000)
		time.sleep(0.05)
		write_data(d3_m2, char_reg, 0b00010000)
		write_data(d3_m4, char_reg, 0b00010000)
		time.sleep(0.05)
		write_data(d3_m3, char_reg, 0b00010000)
		
	else:
		# Blank them all
		blank_display(1)
		blank_display(2)
		blank_display(3)
	
# Reads back the module information from the Smart Nixies [Might be broken some how]
def module_info(disp = 0):
	if(disp == 1):
		print("|_ Reading FW versions")
		core = read_data(d1_m1, fw_core)
		rev = read_data(d1_m1, fw_rev)
		write_data(d1_m1, command_reg, 0xF0)
		addr = read_data(d1_m1, addr_pins)
		print("|__ Module 1")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d1_m2, fw_core)
		rev = read_data(d1_m2, fw_rev)
		write_data(d1_m2, command_reg, 0xF0)
		addr = read_data(d1_m2, addr_pins)
		print("|__ Module 2")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d1_m3, fw_core)
		rev = read_data(d1_m3, fw_rev)
		write_data(d1_m3, command_reg, 0xF0)
		addr = read_data(d1_m3, addr_pins)
		print("|__ Module 3")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d1_m4, fw_core)
		rev = read_data(d1_m4, fw_rev)
		write_data(d1_m4, command_reg, 0xF0)
		addr = read_data(d1_m4, addr_pins)
		print("|__ Module 4")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d1_m5, fw_core)
		rev = read_data(d1_m5, fw_rev)
		write_data(d1_m5, command_reg, 0xF0)
		addr = read_data(d1_m5, addr_pins)
		print("|__ Module 5")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	elif(disp == 2):
		print("|_ Reading FW versions")
		core = read_data(d2_m1, fw_core)
		rev = read_data(d2_m1, fw_rev)
		write_data(d2_m1, command_reg, 0xF0)
		addr = read_data(d2_m1, addr_pins)
		print("|__ Module 1")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d2_m2, fw_core)
		rev = read_data(d2_m2, fw_rev)
		write_data(d2_m2, command_reg, 0xF0)
		addr = read_data(d2_m2, addr_pins)
		print("|__ Module 2")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d2_m3, fw_core)
		rev = read_data(d2_m3, fw_rev)
		write_data(d2_m3, command_reg, 0xF0)
		addr = read_data(d2_m3, addr_pins)
		print("|__ Module 3")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d2_m4, fw_core)
		rev = read_data(d2_m4, fw_rev)
		write_data(d2_m4, command_reg, 0xF0)
		addr = read_data(d2_m4, addr_pins)
		print("|__ Module 4")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d2_m5, fw_core)
		rev = read_data(d2_m5, fw_rev)
		write_data(d2_m5, command_reg, 0xF0)
		addr = read_data(d2_m5, addr_pins)
		print("|__ Module 5")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	elif(disp == 3):
		print("|_ Reading FW versions")
		core = read_data(d3_m1, fw_core)
		rev = read_data(d3_m1, fw_rev)
		write_data(d3_m1, command_reg, 0xF0)
		addr = read_data(d3_m1, addr_pins)
		print("|__ Module 1")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d3_m2, fw_core)
		rev = read_data(d3_m2, fw_rev)
		write_data(d3_m2, command_reg, 0xF0)
		addr = read_data(d3_m2, addr_pins)
		print("|__ Module 2")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d3_m3, fw_core)
		rev = read_data(d3_m3, fw_rev)
		write_data(d3_m3, command_reg, 0xF0)
		addr = read_data(d3_m3, addr_pins)
		print("|__ Module 3")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d3_m4, fw_core)
		rev = read_data(d3_m4, fw_rev)
		write_data(d3_m4, command_reg, 0xF0)
		addr = read_data(d3_m4, addr_pins)
		print("|__ Module 4")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
		
		core = read_data(d3_m5, fw_core)
		rev = read_data(d3_m5, fw_rev)
		write_data(d3_m5, command_reg, 0xF0)
		addr = read_data(d3_m5, addr_pins)
		print("|__ Module 5")
		print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	else:
		print("nixie.module_info says: no argument passed chief...")

# Use this to write a vlue out to a display. [Min value: 00000 Max value: 99999]
# Time between values being written is randomly generated for effect
# Should also turn on the correct comma for numbers >1000 but seems broken
def write_value(value, disp = 0):
	if(value > 99999):
		print("nixie.write_value says: value out of range [++]")
	if(value < -99999):
		print("nixie.write_value says: value out of range [--]")
		
	temp = math.fabs(value)
		
	if(disp == 1):
		m5 = math.floor(temp / 10000)
		#print(m5)
		write_data(d1_m5, command_reg, 0x02)
		if(value < 0):
			#print("we got a minus")
			write_data(d1_m5, char_reg, (0b10000000 | m5))
		else:
			#print("we got a plus")
			write_data(d1_m5, char_reg, m5)
		#write_data(d1_m5, command_reg, 0x02)
		time.sleep(random.random())
		
		m4 = math.floor( (temp - (m5*10000)) / 1000)
		#print(m4)
		write_data(d1_m4, command_reg, 0x02)
		write_data(d1_m4, char_reg, m4)
		#write_data(d1_m4, command_reg, 0x02)
		time.sleep(random.random())
		
		m3 = math.floor( (temp - (m4*1000) - (m5*10000)) / 100)
		#print(m3)
		write_data(d1_m3, command_reg, 0x02)
		if(m3 > 0):
			print("comma needed")
			write_data(d1_m3, char_reg, (m3 | 0b01000000))
		else:
			print("comma not needed")
			write_data(d1_m3, char_reg, m3)
		#write_data(d1_m3, command_reg, 0x02)
		time.sleep(random.random())
		
		m2 = math.floor( (temp - (m3*100) - (m4*1000) - (m5*10000)) / 10)
		#print(m2)
		write_data(d1_m2, command_reg, 0x02)
		write_data(d1_m2, char_reg, m2)
		#write_data(d1_m2, command_reg, 0x02)
		time.sleep(random.random())
		
		m1 = math.floor( (temp - (m2*10) - (m3*100) - (m4*1000) - (m5*10000)) / 1)
		#print(m1)
		write_data(d1_m1, command_reg, 0x02)
		write_data(d1_m1, char_reg, m1)
		#write_data(d1_m1, command_reg, 0x02)

	elif(disp == 2):
		m5 = math.floor(temp / 10000)
		#print(m5)
		write_data(d2_m5, command_reg, 0x02)
		if(value < 0):
			#print("we got a minus")
			write_data(d2_m5, char_reg, (0b10000000 | m5))
		else:
			#print("we got a plus")
			write_data(d2_m5, char_reg, m5)
		#write_data(d2_m5, command_reg, 0x02)
		time.sleep(random.random())
		
		m4 = math.floor( (temp - (m5*10000)) / 1000)
		#print(m4)
		write_data(d2_m4, command_reg, 0x02)
		write_data(d2_m4, char_reg, m4)
		#write_data(d2_m4, command_reg, 0x02)
		time.sleep(random.random())
		
		m3 = math.floor( (temp - (m4*1000) - (m5*10000)) / 100)
		#print(m3)
		write_data(d2_m3, command_reg, 0x02)
		if(m3 > 0):
			print("comma needed")
			write_data(d2_m3, char_reg, (m3 | 0b01000000))
		else:
			print("comma not needed")
			write_data(d2_m3, char_reg, m3)
		#write_data(d2_m3, command_reg, 0x02)
		time.sleep(random.random())
		
		m2 = math.floor( (temp - (m3*100) - (m4*1000) - (m5*10000)) / 10)
		#print(m2)
		write_data(d2_m2, command_reg, 0x02)
		write_data(d2_m2, char_reg, m2)
		#write_data(d2_m2, command_reg, 0x02)
		time.sleep(random.random())
		
		m1 = math.floor( (temp - (m2*10) - (m3*100) - (m4*1000) - (m5*10000)) / 1)
		#print(m1)
		write_data(d2_m1, command_reg, 0x02)
		write_data(d2_m1, char_reg, m1)
		#write_data(d2_m1, command_reg, 0x02)
		
	elif(disp == 3):
		m5 = math.floor(temp / 10000)
		#print(m5)
		write_data(d3_m5, command_reg, 0x02)
		if(value < 0):
			#print("we got a minus")
			write_data(d3_m5, char_reg, (0b10000000 | m5))
		else:
			#print("we got a plus")
			write_data(d3_m5, char_reg, m5)
		#write_data(d3_m5, command_reg, 0x02)
		time.sleep(random.random())
		
		m4 = math.floor( (temp - (m5*10000)) / 1000)
		#print(m4)
		write_data(d3_m4, command_reg, 0x02)
		write_data(d3_m4, char_reg, m4)
		#write_data(d3_m4, command_reg, 0x02)
		time.sleep(random.random())
		
		m3 = math.floor( (temp - (m4*1000) - (m5*10000)) / 100)
		#print(m3)
		write_data(d3_m3, command_reg, 0x02)
		if(m3 > 0):
			print("comma needed")
			write_data(d3_m3, char_reg, (m3 | 0b01000000))
		else:
			print("comma not needed")
			write_data(d3_m3, char_reg, m3)
		#write_data(d3_m3, command_reg, 0x02)
		time.sleep(random.random())
		
		m2 = math.floor( (temp - (m3*100) - (m4*1000) - (m5*10000)) / 10)
		#print(m2)
		write_data(d3_m2, command_reg, 0x02)
		write_data(d3_m2, char_reg, m2)
		#write_data(d3_m2, command_reg, 0x02)
		time.sleep(random.random())
		
		m1 = math.floor( (temp - (m2*10) - (m3*100) - (m4*1000) - (m5*10000)) / 1)
		#print(m1)
		write_data(d3_m1, command_reg, 0x02)
		write_data(d3_m1, char_reg, m1)
		##write_data(d3_m1, command_reg, 0x02)
	else:
		print("nixie.write_value says: no argument passed chief...")

# Starts all of the modules tumbling for effect
# tumble rate is randomly generate for each module every time it is called
def tumble_display(disp = 0):
	if(disp == 1):
		write_data(d1_m1, delay_reg, int((random.random() * 10)))	#sets the count rate
		write_data(d1_m1, command_reg, 0x01)						#starts thew burn in routine
		write_data(d1_m5, delay_reg, int((random.random() * 10)))
		write_data(d1_m5, command_reg, 0x01)
		time.sleep(0.05)
		write_data(d1_m2, delay_reg, int((random.random() * 10)))
		write_data(d1_m2, command_reg, 0x01)
		write_data(d1_m4, delay_reg, int((random.random() * 10)))
		write_data(d1_m4, command_reg, 0x01)
		time.sleep(0.05)
		write_data(d1_m3, delay_reg, int((random.random() * 10)))
		write_data(d1_m3, command_reg, 0x01)
	elif(disp == 2):
		write_data(d2_m1, delay_reg, int((random.random() * 10)))
		write_data(d2_m1, command_reg, 0x01)
		write_data(d2_m5, delay_reg, int((random.random() * 10)))
		write_data(d2_m5, command_reg, 0x01)
		time.sleep(0.05)
		write_data(d2_m2, delay_reg, int((random.random() * 10)))
		write_data(d2_m2, command_reg, 0x01)
		write_data(d2_m4, delay_reg, int((random.random() * 10)))
		write_data(d2_m4, command_reg, 0x01)
		time.sleep(0.05)
		write_data(d2_m3, delay_reg, int((random.random() * 10)))
		write_data(d2_m3, command_reg, 0x01) 
	elif(disp == 3):
		write_data(d3_m1, delay_reg, int((random.random() * 10)))
		write_data(d3_m1, command_reg, 0x01)
		write_data(d3_m5, delay_reg, int((random.random() * 10)))
		write_data(d3_m5, command_reg, 0x01)
		time.sleep(0.05)
		write_data(d3_m2, delay_reg, int((random.random() * 10)))
		write_data(d3_m2, command_reg, 0x01)
		write_data(d3_m4, delay_reg, int((random.random() * 10)))
		write_data(d3_m4, command_reg, 0x01)
		time.sleep(0.05)
		write_data(d3_m3, delay_reg, int((random.random() * 10)))
		write_data(d3_m3, command_reg, 0x01)
	else:
		tumble_display(1)
		tumble_display(2)
		tumble_display(3)