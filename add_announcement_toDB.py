#---------------------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file creates a JSON formated file to push into a DB 
#                The file contains morning announcements
#
# Required libs: 
# Author:        Konstantinos Oikonomou
#
# Created:       13/11/2016
# 
# IMPORTANT NOTICE: In order for the script to work a mongo server must be running localy
#
#---------------------------------------------------------------------------------------------
import csv
from pymongo import MongoClient

#opens the file downloaded from google forms
#replace with your directory
csvfile = open('/Users/amerikanoc/Desktop/Add Announcement.csv', 'r')
reader = csv.reader(csvfile)
#opens the file in which the data will be written in json format
textfile = open('/Users/amerikanoc/Documents/Programming/Python/Smart_School/Testing/announcements.txt', 'a')

#Connect to MongoDB
client = MongoClient()
db = client.test

#This is for the _id of the database
idcount = 1

#iterates through the rows in the csv
#except the first row (data labels)
for row in list(reader)[1:]:
    
    #splits tags and clubs taken from the csv and creates lists
    tags = row[6].split(';') 
    clubs = row[8].split(';')
        
    #creates a document for the DB
    jsonstring = { '_id':'%s' % (str(idcount)), 'author':'%s' % (row[1]), 'date':'%s' % (row[2]), 'title':'%s' % (row[3]), 'text':'%s' % (row[4]), 'target':'%s' % (row[5]), 'tags':tags, 'club':clubs }
    
    #appends the document to the textfile
    textfile.write(str(jsonstring))
    
    #inserts item to the DB's announcements collection
    db.announcements.insert_one(jsonstring)
    
    #increments the _id of the announcement
    idcount += 1
