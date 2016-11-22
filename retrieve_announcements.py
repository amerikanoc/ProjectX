#-----------------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file prints the announcements depending on the student 
#
# Required libs: pymongo
# Author:        Konstantinos Oikonomou
#
# Created:       13/11/2016
#
#IMPORTANT NOTICE: In order for the script to run a mongo server must be running localy
# 
#-----------------------------------------------------------------------------------------
from pymongo import MongoClient
import time

#today's date
#BE CAREFUL with the format
now = time.strftime("%d/%m/%Y")

#connects to the Db
client = MongoClient()
db = client.test

#user inputs his ID
#will be replaced with the QR code
requested_id = input("What is your Anatolia ID?    ")

#pulls student from db
cursor = db.students.find({'_id':'%s'  % (requested_id)})
#dictionary with student's data
mydict = list(cursor)[0]

#the list with the retrieved announcements
wanted = []
#student's interests
interests = mydict['interests']
#student's clubs
clubs = mydict['clubs']

#grades dict for grade-specific announcements (will be used later)
grades = {'4th': ['Lykeion', 'Lykeion & IB', 'All Schools'],
'5th': ['Lykeion', 'Lykeion & IB', 'All Schools'],
'6th': ['Lykeion', 'Lykeion & IB', 'All Schools'],
'IB1': ['IB', 'Lykeion & IB', 'All Schools'],
'IB2': ['IB', 'Lykeion & IB', 'All Schools']}

#associates student's grade with grades list
stgrade = grades['%s' % mydict['grade']]

#pulls only TODAY's announcements, which are available for the specific GRADE LIST
cursor = db.announcements.find({'date':'%s' % (now), '$or': [{'target':'%s' % (stgrade[0])}, {'target':'%s' % (stgrade[1])}, {'target':'%s' % (stgrade[2])}]})
announcements = [d for d in cursor]

#takes the announcement ID's
for item in announcements:
    wanted += [item['_id'] for tag in item['tags'] if tag in interests]
    wanted += [item['_id'] for club in item['club'] if club in clubs]

#prints the announcement ID's
print(list(set(wanted)))