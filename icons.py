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
from os import listdir
from pymongo import MongoClient


#### VARIABLES #########################################################
#DB_MONGO_IP = "127.0.0.1"
DB_MONGO_IP = "192.168.28.248"
DB_MONGO_PORT = 27017
DB_MONGO_NAME = "kyros"

########################################################################

########################################################################

def new_icon(type, subtype, fileName, svg):
	con = MongoClient(DB_MONGO_IP, int(DB_MONGO_PORT))
	db = con[DB_MONGO_NAME]
	icon_collection = db['ICON']
	icon = {
    "type" : type,
    "subtype" : subtype,
    "file_name" : fileName,
    "svg" : svg
	}
	icon_collection.save(icon)

def leer_svg(fichero):
    #str = open(fichero, 'r').read()
    #return str
    enc = "latin-1"
    f = open(fichero, "r")
    content = f.read() # raw encoded content
    u_content = content.decode(enc) # decodes from enc to unicode
    utf8_content = u_content.encode("utf8")
    return utf8_content

########################################################################

########################################################################

for file_name in listdir("./events"):
    svg = leer_svg("./events/"+file_name)
    new_icon(1, 0, file_name, svg)

