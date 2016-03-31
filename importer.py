#!/usr/bin/python
# Slack export file parser
# Written by Jacob Rickerd
# This program is used to import a slack export folder into a MongoDB  
# database
# Written with Python 2.7

#imports required packages
import json
import re
from pymongo import MongoClient
import os
import sys
import zipfile

path = sys.argv[1]

#Creates MongoDB Client
client = MongoClient()
client = MongoClient('localhost', 27017)

#Creates MongoDB database and collection
db = client.test_database
collection = db.test_collection

#Creates the docuements, I believe?
posts = db.posts
users = db.users

#Inits the dictionary with a dummy value
usersDict = {'key':'value'}

#posts.drop()
#users.drop()

#Adds the usernames and user ids into the database
def addUsers(usersJSON):
	with open(usersJSON, 'r') as f:
		data = json.load(f)
		
	for i in data:
		for key, value in i.iteritems():
			if (key == "id"):
				numberID =  value
			if (key == "name"):
				nameID = value
		usersDict[numberID] = nameID
	
	#users.insert(usersDict)
	users.insert_many(data)

#Imports all the .json files in the folder
def importChannels():
	
	zip_ref = zipfile.ZipFile(path, 'r')
	zip_ref.extractall("/tmp/SlackDump/")
	zip_ref.close()

	extractPath = "/tmp/SlackDump"

	for item in os.listdir(extractPath):
	
		if ((re.search(".json", item) is None) and item != "bots"):

			for filename in os.listdir((extractPath + "/" + item)):
				directory = extractPath + "/" + item + "/" + filename
				print directory

				#Imports JSON file into 'data', which is a list of dictionaries
				with open(directory, 'r') as f:
					data = json.load(f)
		
				for i in data:
					i['channel'] = item
				posts.insert_many(data)
		elif (item == "users.json"):
			jsonfile = extractPath + "/" + item
			addUsers(jsonfile)
		
importChannels()
print "There are", posts.count(), "posts!"
print "There are", users.count(), "users!"


