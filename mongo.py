#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pymongo

MONGODB_HOST = '192.168.28.248'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 1000
MONGODB_DATABASE = 'demos'


URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

try:
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as error:
    print 'Error with mongoDB connection: %s' % error
except pymongo.errors.ConnectionFailure as error:
    print 'Could not connect to MongoDB: %s' % error

def getMongoDBConnection():
    return client[MONGODB_DATABASE]
