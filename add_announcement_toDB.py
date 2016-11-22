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
import urllib.request
import os
from pymongo import MongoClient

#opens the file downloaded from google forms
#replace with your directory
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQj38RN_Ig0E_6q3BuW_woaP2ob4E1jZvDqdJECZlNIt7ToJHtbMW9XpKYlVrzdaEDQ2RMTqJTwZVm5/pub?output=csv'
urllib.request.urlretrieve(url, 'Add Announcement.csv')
csvfile = open('Add Announcement.csv', 'r')
reader = csv.reader(csvfile)
#opens the file in which the data will be written in json format
textfile = open('announcements.txt', 'a')

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

os.remove('Add Announcement.csv')