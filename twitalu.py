#!/usr/bin/env python3

# 'tweet_queue' when returned will contain only the valid tweets .'work' when 
# returned contains the validated commands from the scrubber. It is directly 
# related to 'tweet_queue' so tweet_queue[0] and work[0] relate to the same job
# this must be maintained for the responder to work properly. work[i] has 5 parts
# work[i][0] = {the valid string as matched by the reg ex}
# work[i][1] = {the valid A part}
# work[i][2] = {the valid operation part}
# work[i][3] = {the valid B part}
# work[i][4] = {is empty but will have xxxxx placed here to indicate the solution as a string}
# work[i][5] = {is empty but will have xxxxx placed here to indicate the solution as an int}
# 

import twy_twitter as twitter
import twitalu_globals as globals
import twitalu_init as init
import twitalu_OPCODE_display as OPCODE_display
import nixie
import time
if globals.no_hardware == True:
	import twitalu_Math_dev as tMath
	nixie.init()
else:
	import twitalu_Math as tMath
	init.init()

while(1):
	nixie.tumble_display()
	OPCODE_display.display_twit_check()
	time.sleep(4)
	
	tweets = twitter.get_tweets()
	
	[tweet_queue, work] = twitter.input_scrub(tweets)
	
	try:
		print()
		work_keys = list(work.keys())
		print("Current work queue keys: {0}".format(work_keys))
		final_key = work_keys[(len(work)) - 1]
	except:
		final_key = 0
		
	print("Final Key: {0}".format(final_key))
	
	print()
	print("***Processing Work***")
	
	if len(work) > 0:
		for i in range(0, int(final_key) + 1):
			print("|_ Job number: {0}".format(i))
			OPCODE_display.display_twitalu()
			nixie.tumble_display()
			time.sleep(2)
			
			try:
				print("|__ Raw work: {0}".format(work[i]["0"]))
				nixie.write_value(int(work[i]["1"]), 1)
				time.sleep(2)
				
				# Decode operation and display on LED matrix
				if work[i]["2"] == "+":
					OPCODE_display.display_ADD()
				elif work[i]["2"] == "-":
					OPCODE_display.display_SUB()
				elif work[i]["2"] == "*":
					OPCODE_display.display_MUL()
				elif work[i]["2"] == "/":
					OPCODE_display.display_DIV()
				elif work[i]["2"] == "AND":
					OPCODE_display.display_AND()
				elif work[i]["2"] == "OR":
					OPCODE_display.display_OR()
				elif work[i]["2"] == "XOR":
					OPCODE_display.display_XOR()
				elif work[i]["2"] == "ROR":
					OPCODE_display.display_ROR()
				elif work[i]["2"] == "ROL":
					OPCODE_display.display_ROL()
				
				time.sleep(2)
				nixie.write_value(int(work[i]["3"]), 2)
				time.sleep(2)
				
				print("|___ Action: Perform calculation")
				result = tMath.calculate(work[i]["1"],work[i]["2"],work[i]["3"])
				print("|____ Result: {0}".format(result))
				print("|_____ Action: Format for insertion")
				result_str = "{0}".format(result)
				print("|______Result: {0}".format(result_str))
				work[i]["4"] = result_str
				work[i]["5"] = result
				nixie.write_value(int(work[i]["5"]), 3)
				time.sleep(5)
			except:
				print("|__ Job empty.")
				print("|___ Conclusion: Job scrubbed")
	else:
		print("|_ Job queue empty.")
		print("|__ Conclusion: No work")
	
	twitter.send_response(tweet_queue, work, final_key)