#-------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file prints the announcements depending on the student 
#
# Required libs: pymongo
# Author:        Konstantinos Oikonomou
#
# Created:       13/11/2016
# 
#-------------------------------------------------------------------------------
from pymongo import MongoClient
import time

now = time.strftime("%Y-%m-%d")

client = MongoClient()
db = client.test

requested_id = input("What is your Anatolia ID?    ")

cursor = db.students.find({'_id':'%s'  % (requested_id)})
mydict = list(cursor)[0]

wanted = []
interests = mydict['interests']
clubs = mydict['clubs']

grades = {'4th': ['Lykeion', 'Lykeion & IB', 'All Schools'],
'5th': ['Lykeion', 'Lykeion & IB', 'All Schools'],
'6th': ['Lykeion', 'Lykeion & IB', 'All Schools'],
'IB1': ['IB', 'Lykeion & IB', 'All Schools'],
'IB2': ['IB', 'Lykeion & IB', 'All Schools']}

stgrade = grades['%s' % mydict['grade']]

cursor = db.announcements.find({'date':'%s' % (now), '$or': [{'target':'%s' % (stgrade[0])}, {'target':'%s' % (stgrade[1])}, {'target':'%s' % (stgrade[2])}]})
announcements = [d for d in cursor]

for item in announcements:
    wanted += [item['_id'] for tag in item['tags'] if tag in interests]
    wanted += [item['_id'] for club in item['club'] if club in clubs]


print(list(set(wanted)))