# Input: list of n people (name, address, attendance)
# Output: 
# 	- Email to each person of their partner + address + date
# 	- Email to one person with all information

# Author: Aysha Habbaba
# Date: 12/1
##################

import csv, random, smtplib, constants

# read in + parse CSV
# TODO: what's the format of each deet in deets?
def read_csv(filename):
	deets = []
	with open(filename, "r") as f:
		content = csv.reader(f)
		next(content)
		for c in content:
			deets.append(c)

	return(deets)

# assign folks 
def assign_giftees(smtp_session, peeps):
	gifted = []
	possible_giftees = peeps[:]
	summary_message = "A summary of giftees and gifters:\n"
	for p, peep in enumerate(peeps):
		# remove current gifter as a possible giftee
		if (len(possible_giftees) != 1 and possible_giftees[0][1] == peep[1]): del possible_giftees[0]

		# randomly pick a giftee from pool
		rand = random.randint(0, len(possible_giftees) - 1)	

		# send mail to gifter
		text =  ("Welcome to the first ever salam halal pair-based gift exchange " +
					peep[1] + "!!!!!!!\n\n" +
       			    "Your assigned secret giftee is " +
       				possible_giftees[rand][1] + " *cue excitement and joy* \n\n" +
       				"After doing some very complicated maths, lots of calculations and " + 
					"emphatically x-ing out dates, gift exchange will take place on *DECEMBER 8th* during our weekly Wednesday night book exchange. " +
					"Reminder that we have a $30 cap on gift value.\n\n" +
					"Have a non-denominational, completely non-offensive, totally generic and politically correct winter!")

		message = 'Subject: {}\n\n{}'.format("SSS Gift Exchange!", text)
		send_mail(smtp_session, peep[2], message)

		# append to gift exchange summary 
		summary_message += (peep[1] + " gives to " + possible_giftees[rand][1] + "\n")
		
		# remove giftee from giftee pool
		gifted.append(possible_giftees[rand])
		del possible_giftees[rand]

		# add current gifter back to giftee pool if they haven't already gotten a gift
		# (ik, horrid complexity)
		if (not(peep in gifted)): possible_giftees.append(peep)

	return summary_message

def setup_mail():
	s = smtplib.SMTP(constants.SMTP_SERVER, constants.SMTP_PORT)
	s.starttls()
	s.login(constants.SENDER_EMAIL, constants.SENDER_PASSWORD)
	return s

def send_mail(smtp_session, receiver, message):
	smtp_session.sendmail(constants.SENDER_EMAIL, receiver, message)

def close_mail_session(smtp_session):
	smtp_session.quit()

# send summary of gift exchange (who is gifting who) to two additional parties
def email_n_parties_summaries(smtp_session, summary):
	send_mail(smtp_session, constants.THIRD_PARTY_EMAIL, summary)
	send_mail(smtp_session, constants.FOURTH_PARTY_EMAIL, summary)

# bb driver (icu ansel)
names = read_csv(constants.FILENAME)
s = setup_mail()
summary = assign_giftees(s, names)
email_n_parties_summaries(s, summary)
close_mail_session(s)
