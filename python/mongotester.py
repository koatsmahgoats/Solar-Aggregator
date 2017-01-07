# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:44:10 2016

@author: Koats
"""
from sys import *
from math import *
from pymongo import MongoClient
import pymongo
import bson

result = [[0,1,1,1,1],[1,1,1,1,3]]
string_num = []

client = MongoClient()  # On local client
dbName = 'test'
dbCollection = 'wtf'
db = client[dbName]
runsCollection = db[dbCollection]

db.runsCollection.delete_many({})
    #solution.display()  # keep this for now just in case
solutionDict = {}
#solutionNumberStr = str(solutionNumber)
#solutionDict['_id'] = solutionNumberStr
solutionVariableList = result[0]
solutionObjectiveList = result[1]
solutionDict["variables"] = solutionVariableList
solutionDict["objectives"] = solutionObjectiveList

doc_id = db.runsCollection.insert_one(solutionDict)

    
cursor = db.runsCollection.find(projection = {'objectives': False, '_id':False})
for document in cursor:
    print(document['variables'])