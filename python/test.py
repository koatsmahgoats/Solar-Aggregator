from sys import *
from math import *
from borg import *
from pymongo import MongoClient
import pymongo
import bson

nvars = 11
nobjs = 2
k = nvars - nobjs + 1


def DTLZ2(*vars):
	g = 0

	for i in range(nvars-k, nvars):
		g = g + (vars[i] - 0.5)**2

	objs = [1.0 + g]*nobjs

	for i in range(nobjs):
		for j in range(nobjs-i-1):
			objs[i] = objs[i] * cos(0.5 * pi * vars[j])
		if i != 0:
			objs[i] = objs[i] * sin(0.5 * pi * vars[nobjs-i-1])

	return objs


string_num = []
mod_num = []

client = MongoClient()  # On local client
dbName = 'test'
dbCollection = 'test_coll_DTLZ3'
db = client[dbName]
runsCollection = db[dbCollection]
db.runsCollection.delete_many({})
borg = Borg(nvars, nobjs, 0, DTLZ2)
borg.setBounds(*[[0, 1]]*nvars)
borg.setEpsilons(*[0.01]*nobjs)

result = borg.solve({"maxEvaluations":100})

solutionNumber = 1
for solution in result:
    #solution.display()  # keep this for now just in case
    solutionDict = {}
#    solutionNumberStr = str(solutionNumber)
#    solutionDict['_id'] = solutionNumberStr
    solutionVariableList = solution.getVariables()
    solutionObjectiveList = solution.getObjectives()
    print(solutionVariableList)
    solutionDict["variables"] = solutionVariableList
    solutionDict["objectives"] = solutionObjectiveList
    print(solutionDict)
    #print(solutionDict['variables'])
    solutionNumber += 1
    doc_id = db.runsCollection.insert_one(solutionDict)

string_num = []
total_num = []
cursor = db.runsCollection.find(projection = {'objectives': False, '_id':False})
for document in cursor:
    string_num.append(document['variables'])
    print("This is string" + str(string_num))
    for part in string_num:
        total_num = (str(string_num(part[0])))
    print (sum(total_num))
    
    
 #   print(varlist)
#    string_num.append(docsol[])
#    mod_num.append(docsol[1])