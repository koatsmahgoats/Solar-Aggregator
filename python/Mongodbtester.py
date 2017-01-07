# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:29:53 2016

@author: Koats
"""


from pymongo import MongoClient
from datetime import datetime


client = MongoClient()  # On local client
dbName = 'test'
dbCollection = 'restaurants'
db = client[dbName]
runsCollection = db[dbCollection]



result = db.restaurants.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    })
    
cursor = db.restaurants.find()
for document in cursor:
    print(document)