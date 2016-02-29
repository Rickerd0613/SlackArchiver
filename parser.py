#!/usr/bin/python
# Slack export file parser
# Written by Jacob Rickerd
# This program is used to query a MongoDB database for Slack export  
# messages
# Written with Python 2.7

#imports required packages
import json
import re
from pymongo import MongoClient
import os
import calendar
from datetime import timedelta
import datetime
import sys

#Creates MongoDB Client
client = MongoClient()
client = MongoClient('localhost', 27017)

#Creates MongoDB database and collection
db = client.test_database
collection = db.test_collection

#Creates the docuements, I believe?
posts = db.posts
users = db.users

#Translates user id to username and vice versa
def translateUsername(data):
	user = list(users.find({"key": "value"}))
	for i in user:
		for key, value in i.iteritems():
			if (key == data):
				return value
			if (value == data):
				return key

#Translates the timestamp from seconds to a readable timestamp
#Can be off an hour due to DST
def tsToTime(ts):
    time = datetime.datetime.fromtimestamp(ts)
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(time.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert time.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=time.microsecond)

#Prints recursive lists and dictionaries to the screen
def enumListOrDict(key, value):
	if (type(value) == list):
		print key + ":"
		for i in value:
			if (type(i) == unicode):
				print "\t\t", i
			else:
				for itemOne, itemTwo in i.iteritems():
					#print "\t" + itemOne + ":", itemTwo
					print "\t",
					enumListOrDict(itemOne, itemTwo)
	elif (type(value) == dict):
		print key + ":"
		for itemOne, itemTwo in value.iteritems():
			#print "\t" + itemOne + ":", itemTwo
			print "\t",
			enumListOrDict(itemOne, itemTwo)
	else:
		print key + ":", value

#Gets the field being searched for
print "Please enter your search parameters below"
print "All fields accept regex besides username"
print "Press enter for nil"
textInput = raw_input('Please enter the message text: ')
usernameInput = translateUsername(raw_input('Please enter the username: '))
channelInput = raw_input('Please enter the channel: ')

#Handels all the possiable options for the input fields
if (textInput and usernameInput and channelInput):
	search = list(posts.find({"text": {"$regex": textInput, "$options": 'i'}, "user": usernameInput, "channel": {"$regex": channelInput, "$options": 'i'}}))
elif (textInput and usernameInput):
	search = list(posts.find({"text": {"$regex": textInput, "$options": 'i'}, "user": usernameInput}))
elif (textInput and channelInput):
	search = list(posts.find({"text": {"$regex": textInput, "$options": 'i'}, "channel": {"$regex": channelInput, "$options": 'i'}}))
elif (usernameInput and channelInput):
	search = list(posts.find({"user": usernameInput, "channel": {"$regex": channelInput, "$options": 'i'}}))
elif (textInput):
	search = list(posts.find({"text": {"$regex": textInput, "$options": 'i'}}))
elif (usernameInput):
	search = list(posts.find({"user": usernameInput}))
elif (channelInput):
	search = list(posts.find({"channel": {"$regex": channelInput, "$options": 'i'}}))
else:
	sys.exit("EXITING: Please enter data next time")

#Prints the dictionaries held within the list
for i in search:
    print "---------------------------------"
    for key, value in i.iteritems():
		if (key == "user"):
			print key + ":", translateUsername(value)
		elif (key == "ts"):
			print key + ":", tsToTime(float(value))
		elif (key == "_id"):
			continue
		elif (type(key) == list or dict):
			enumListOrDict(key, value)
		else:
			print key + ":", value
