#!/usr/bin/env python3

import sys
# appends to PYTHONPATH the location of the example codes
sys.path.append(r'/home/pi/git/quick2wire-python-api/')

import quick2wire.i2c as i2c
import time

# Here the address that the port expander is at is set
address_1 = 0x08
address_2 = 0x09
address_3 = 0x0a
address_4 = 0x0b
address_5 = 0x0c

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

# This function writes a value into a register 
def write_register(bus, addr, reg, b):
	bus.transaction(
	i2c.writing_bytes(addr, reg, b))

# This function reads a value from a register
def read_register(bus, addr, reg):
	return bus.transaction(
	i2c.writing_bytes(addr, reg),
	i2c.reading(addr, 1))[0][0]
	
def blank_display():
	write_register(bus, address_1, char_reg, 0b00010000)
	write_register(bus, address_5, char_reg, 0b00010000)
	time.sleep(0.05)
	write_register(bus, address_2, char_reg, 0b00010000)
	write_register(bus, address_4, char_reg, 0b00010000)
	time.sleep(0.05)
	write_register(bus, address_3, char_reg, 0b00010000)
	
def module_info():
	print("|_ Reading FW versions")
	core = read_register(bus, address_1, fw_core)
	rev = read_register(bus, address_1, fw_rev)
	write_register(bus, address_1, command_reg, 0xF0)
	addr = read_register(bus, address_1, addr_pins)
	print("|__ Module 1")
	print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	
	core = read_register(bus, address_2, fw_core)
	rev = read_register(bus, address_2, fw_rev)
	write_register(bus, address_2, command_reg, 0xF0)
	addr = read_register(bus, address_2, addr_pins)
	print("|__ Module 2")
	print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	
	core = read_register(bus, address_3, fw_core)
	rev = read_register(bus, address_3, fw_rev)
	write_register(bus, address_3, command_reg, 0xF0)
	addr = read_register(bus, address_3, addr_pins)
	print("|__ Module 3")
	print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	
	core = read_register(bus, address_4, fw_core)
	rev = read_register(bus, address_4, fw_rev)
	write_register(bus, address_4, command_reg, 0xF0)
	addr = read_register(bus, address_4, addr_pins)
	print("|__ Module 4")
	print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	
	core = read_register(bus, address_5, fw_core)
	rev = read_register(bus, address_5, fw_rev)
	write_register(bus, address_5, command_reg, 0xF0)
	addr = read_register(bus, address_5, addr_pins)
	print("|__ Module 5")
	print("|___ Core: {0} Version:{1} Address:{2}".format(core, rev, addr))
	

# The main parts of the program start here
with i2c.I2CMaster() as bus:
	
	print("-> Program Starting")
	module_info()
	time.sleep(1)
	
	for q in range (0, 10):
		write_register(bus, address_5, char_reg, q)
		
		for w in range (0, 10):
			write_register(bus, address_4, char_reg, w)
			
			for e in range (0,10):
				write_register(bus, address_3, char_reg, e)
				
				for r in range (0, 10):
					write_register(bus, address_2, char_reg, r)
				
					for t in range (0, 10):
						write_register(bus, address_1, char_reg, t)
						#time.sleep(0.05)
	
	time.sleep(1)
	blank_display()
