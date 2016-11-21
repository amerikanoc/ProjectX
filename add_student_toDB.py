#--------------------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file creates a JSON formated file to push into a DB 
#                The file contains student data
#
# Required libs: 
# Author:        Konstantinos Oikonomou
#
# Created:       03/11/2016
# 
# IMPORTANT NOTICE: In order for the script to work a mongo server must be running localy
#
#---------------------------------------------------------------------------------------------

import csv
from pymongo import MongoClient

#opens the file downloaded from google forms
#replace with your directory
csvfile = open('/Users/amerikanoc/Desktop/Project X.csv', 'r')
reader = csv.reader(csvfile)
#opens the file in which the data will be written in json format
#the file is opened in appending mode
textfile = open('/Users/amerikanoc/Documents/Programming/Python/Smart_School/Testing/students.txt', 'a')

#Connect to MongoDB
client = MongoClient()
db = client.test

#iterates through the rows in the csv
#except the first row (data labels)
for row in list(reader)[1:]:
    
    #splits classes, clubs, interests taken from the csv and creates lists
    classes = row[5].split(';')
    clubs = row[6].split(';')
    interests = row[7].split(';')
    #concatanates the first and last name from csv
    full_name = "{} {}".format(row[2], row[3])

    #creates a document for the DB    
    jsonstring = { '_id':'%s' % (row[1]), 'name':'%s' % (full_name), 'grade':'%s' % (row[4]), 'classes':classes, 'interests':interests, 'clubs':clubs }
    
    #appends the document to the textfile
    textfile.write(str(jsonstring))
    
    #inserts the file to the DB's students collection
    db.students.insert_one(jsonstring)
