#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# autor: Carlos Rueda
# date: 2016-11-25
# version: 1.1

##################################################################################
# version 1.0 release notes: extract data from MySQL and generate json
# Initial version
# Requisites: library python-mysqldb. To install: "apt-get install python-mysqldb"
##################################################################################

import logging, logging.handlers
import os
import json
import sys
import datetime
import calendar
import time
import json
from pymongo import MongoClient


#### VARIABLES #########################################################
#DB_MONGO_IP = "127.0.0.1"
DB_MONGO_IP = "192.168.28.248"
DB_MONGO_PORT = 27017
DB_MONGO_NAME = "kyros"

########################################################################

########################################################################

def new_notification(eventType, eventId):
	con = MongoClient(DB_MONGO_IP, int(DB_MONGO_PORT))
	db = con[DB_MONGO_NAME]
	monitor_collection = db['APP_NOTIFICATIONS']
	notification = {
    "username" : "test",
    "geocoding" : "Calle Torre de Don Miguel, 13, 28031 Madrid, España",
    "battery" : 100,
    "timestamp" : 1480404039000,
    "altitude" : 765,
    "heading" : 0,
    "subtype" : eventType,
    "location" : {
        "type" : "Point",
        "coordinates" : [ 
            -3.645441, 
            40.373516
        ]
    },
    "tracking_id" : 36441485,
    "vehicle_license" : "1615-FDW",
    "type" : 1,
    "id" : eventId,
    "speed" : 100
	}
	monitor_collection.save(notification)

########################################################################

########################################################################
contador_eventType = 1051
contador_eventId = 998978592

for i in range (5):
	new_notification(contador_eventType, contador_eventId)
	contador_eventType +=1
	contador_eventId +=1
