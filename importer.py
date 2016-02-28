#!/usr/bin/python

import json
import re
from pymongo import MongoClient
import os
import sys

path = sys.argv[1]

#Creates MongoDB Client
client = MongoClient()
client = MongoClient('localhost', 27017)

#Creates MongoDB database and collection
db = client.test_database
collection = db.test_collection

#idk really, i googed all this crap
posts = db.posts

users = db.users

usersDict = {'key':'value'}

#posts.drop()
#users.drop()

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
	
	users.insert(usersDict)

#Imports all the .json files in the folder
for item in os.listdir(path):
	
	if ((re.search(".json", item) is None) and item != "bots"):

		for filename in os.listdir((path + "/" + item)):
			directory = path + "/" + item + "/" + filename
			print directory

			#Imports JSON file into 'data', which is a list of dictionaries
			with open(directory, 'r') as f:
				data = json.load(f)
		
			for i in data:
				i['channel'] = item
			posts.insert_many(data)
	elif (item == "users.json"):
		jsonfile = path + "/" + item
		addUsers(jsonfile)
		

print "There are", posts.count(), "posts!"
print "There are", users.count(), "users!"


