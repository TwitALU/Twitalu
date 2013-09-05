#!/usr/bin/env python3

from twython import Twython, TwythonError
import twitalu_OPCODE_display as OPCODE_display
from hashids import Hashids
import nixie
import re
import time

# Let's initialise some objects that we need. Yes, i know about the has salt. I had to.
twitter = Twython('74GqRHU1JaPvrKx6SHQ4w', '3EL0biFCRuJGLf5ttZ3W6T6ovMsd2JoK3H1QM9GE', '1543952911-NFuG7CC8KF4NxdudU5ZNBlZcNmRhoCPJY673Ehk', 'hCkiPne3tBxlRQ4Qr9UKer0Op8tqwH5QZIu6OilPnU')
hashids = Hashids(salt='OUTATIME')
re_cmd = re.compile('@twittithmetic\s*(\d+)\s*([\+]|[\-]|[\/]|[\*]|AND|OR|XOR|ROR|ROL)\s*(\d+)\s*',re.IGNORECASE)

def get_tweets():
	# Initialise the object for storing tweets that need processing and open the last_id processed file
	# If starting the system after a long down time it is recomended to blank the last_id file to a single space character
	# We could do it as a cron job to be honest or something like that
	id_file = open("last_id.txt", "rt")
	last_id = id_file.read()
	id_file.close()
	
	tweets = {}
	tweet_number = 0
	
	print()
	print("***Retrieveing Timelines***")

	if last_id == ' ':
		# If there is no last id stored in the file then it get the last 50 tweets for the following API calls
		# Fetches the last 50 tweets on home timeline (i.e. responses that have been sent)
		#since_id='0'
		try: 
			home_timeline = twitter.get_home_timeline(screen_name='twittithmetic', count='50')
		except TwythonError as e:
			print(e)

		# Fetches the last 50 mentions (i.e. things we have to process)
		#since_id='0'
		try: 
			mentions_timeline = twitter.get_mentions_timeline(screen_name='twittithmetic', count='50')
		except TwythonError as e:
			print(e)
	else:
		# If there is a last id stored in the file then 50 tweets after this are requested for the following API calls
		# Fetches the last 50 tweets on home timeline (i.e. responses that have been sent)
		try: 
			home_timeline = twitter.get_home_timeline(screen_name='twittithmetic', count='50', since_id = last_id)
		except TwythonError as e:
			print(e)

		# Fetches the last 50 mentions (i.e. things we have to process)
		try: 
			mentions_timeline = twitter.get_mentions_timeline(screen_name='twittithmetic', count='50', since_id = last_id)
		except TwythonError as e:
			print(e)

	# Comparing the retrieved lists
	# First loop selects a job from the mentions list	
	for x in range(0, len(mentions_timeline)):
		print("|_ Looking for job ID: {0}".format(mentions_timeline[x]["id_str"]))
		tweet_flag = 0
		
		#Second loop scans through the list of job responses that have been sent
		for y in range(0, len(home_timeline)):
			#print("checking response ID: {0}".format(home_timeline[y]["in_reply_to_status_id_str"]))
			if home_timeline[y]["in_reply_to_status_id_str"] == mentions_timeline[x]["id_str"]:
				# If the id is seen in both lists then mark it as done.
				print("|__ ID match found. Job complete: {0}".format(mentions_timeline[x]["id_str"]))
				tweet_flag = 1
		
		# If the flag isn't set after checking all responses then the job of interest hasn't been processed yet
		if tweet_flag == 0:
			print("|__ No ID match found. Job not complete: {0}".format(mentions_timeline[x]["id_str"]))
			tweets[tweet_number] = mentions_timeline[x]
			tweet_number = tweet_number + 1
			
	print()
	print("***Tweet queue***")
	for z in range(0, len(tweets)):
		print(tweets[z]["text"])
	
	if len(tweets) > 0:
		print()
		print("Storing last job ID: {0}".format(tweets[0]["id"]))
		id_file = open("last_id.txt", "wt")
		id_file.write(tweets[0]["id_str"])
		id_file.close()
	
	return tweets
		
def send_response(tweet_queue, work, final_key):
	# This could cause a problem as the system will sit in here sending responses for potentially a long time.
	# Not alot can be done as we're rate limited by the Twitter API anyway so it takes as long as it takes.
	
	print()
	print("***Processing Responses***")
	
	
	if len(work) > 0:
		for i in range(0, int(final_key) + 1):
			print("|_ Job number: {0}".format(i))
			try:
				tweet_author = tweet_queue[i]["user"]
				tweet_author_screen_name = tweet_author["screen_name"]
				tweet_author_name = tweet_author["name"]
				mention_id_hash = hashids.encrypt(tweet_queue[i]["id"])[0:8]
				
				status_update = "@{0} Hello {1}, Your solution is {3} [{2}]".format(tweet_author_screen_name, tweet_author_name, mention_id_hash, work[i]["4"])
					
				print("|__ Mention ID: {0}  Mention ID Hash: {1}".format(tweet_queue[i]["id_str"], mention_id_hash))
				print("|__ Input from: @{0} Content: {1}".format(tweet_author_screen_name, tweet_queue[i]["text"]))	
				print("|___ Response generated: {0}".format(status_update))
				
				time.sleep(2)
				OPCODE_display.display_twit_send()
				time.sleep(4)
				
				try:
					twitter.update_status(in_reply_to_status_id = tweet_queue[i]["id_str"], status = status_update)
				except TwythonError as e:
					print(e)
					
			except:
				print("|__ No work at this position.")
				print("|___ Conclusion: Work exists later in queue")
			
			OPCODE_display.display_wait()
			time.sleep(3)
			OPCODE_display.countdown(0x11)
			time.sleep(17)
			
	else:
		print("|_ Response queue empty.")
		print("|__ Conclusion: No responses")
					
	if len(work) == 0:
		OPCODE_display.display_wait()
		time.sleep(3)
		OPCODE_display.countdown(0x4B)
		time.sleep(75)
		
def input_scrub(tweets):
	job_number = len(tweets)
	scrubbed_jobs = tweets
	commands = {}
	temp = {}
	
	print()
	print("***Scrubbing Tweets***")
	
	for i in range(0, len(tweets)):
		print("|_ Job number: {0}".format(i))
		cmd_in = tweets[i]["text"]
		try:
			cmd = re_cmd.search(cmd_in)
			print("|__ Group 0: {0}".format( cmd.group(0) ))
			temp["0"] = cmd.group(0)
			print("|__ Group 1: {0}".format( cmd.group(1) ))
			temp["1"] = cmd.group(1)
			print("|__ Group 2: {0}".format( cmd.group(2) ))
			temp["2"] = cmd.group(2)
			print("|__ Group 3: {0}".format( cmd.group(3) ))
			temp["3"] = cmd.group(3)
			temp["4"] = '0'
			temp["5"] = '0'
			commands[i] = {}
			commands[i].update(temp)
		except:
			print("|__ Reg Ex did not match.")
			print("|___ Conclusion: No valid command")
			del scrubbed_jobs[i]
			print("|____ Action: Job Scrubbed.")
		
	if job_number == 0:
		print("|_ Tweet queue empty.")
		print("|__ Conclusion: No Tweets")

	return (scrubbed_jobs, commands)
	