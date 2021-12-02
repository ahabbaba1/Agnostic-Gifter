# Input: list of n people (name, address, attendance)
# Output: 
# 	- Email to each person of their partner + address + date
# 	- Email to one person with all information

# Author: Aysha Habbaba
# Date: 12/1
##################

import csv
import random

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
	possibleGiftees = peeps[:]
	for p, peep in enumerate(peeps):
		# remove current gifter as a possible giftee
		if (len(possibleGiftees) != 1 and possibleGiftees[0][1] == peep[1]): del possibleGiftees[0]

		# randomly pick a giftee from pool
		rand = random.randint(0, len(possibleGiftees) - 1)	
		print(peep[1], "gives to ", possibleGiftees[rand][1])
		
		# remove giftee from giftee pool
		gifted.append(possibleGiftees[rand])
		del possibleGiftees[rand]

		# add current gifter back to giftee pool if they haven't already gotten a gift
		# (ik, horrid complexity)
		if (not(peep in gifted)):  possibleGiftees.append(peep)


# send email


# bb driver (icu ansel)
names = read_csv("strings.csv")
assign_giftees(names)
