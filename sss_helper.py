# Input: list of n people (name, address, attendance)
# Output: 
# 	- Email to each person of their partner + address + date
# 	- Email to one person with all information

# Author: Aysha Habbaba
# Date: 12/1
##################

import csv, random, smtplib, constants

# read in + parse CSV
def read_csv(filename):
	deets = []
	with open(filename, "r") as f:
		content = csv.reader(f)
		next(content)
		for c in content:
			deets.append(c)

	return(deets)

# assign folks 
def assign_giftees(peeps):
	gifted = []
	possible_giftees = peeps[:]
	for p, peep in enumerate(peeps):
		# remove current gifter as a possible giftee
		if (len(possible_giftees) != 1 and possible_giftees[0][1] == peep[1]): del possible_giftees[0]

		# randomly pick a giftee from pool
		rand = random.randint(0, len(possible_giftees) - 1)	
		# print(peep[1], "gives to ", possible_giftees[rand][1])
		
		# remove giftee from giftee pool
		gifted.append(possible_giftees[rand])
		del possible_giftees[rand]

		# add current gifter back to giftee pool if they haven't already gotten a gift
		# (ik, horrid complexity)
		if (not(peep in gifted)): possible_giftees.append(peep)

def setup_mail():
	s = smtplib.SMTP(constants.SMTP_SERVER, constants.SMTP_PORT)
	s.starttls()
	s.login(constants.SENDER_EMAIL, constants.SENDER_PASSWORD)

def send_mail(smtp_session, receiver, message):
	smtp_session.sendmail(constants.SENDER_EMAIL, receiver, message)

def close_smtp_session(smtp_session):
	smtp_session.quit()
	
# bb driver (icu ansel)
names = read_csv(constants.FILENAME)
assign_giftees(names)
