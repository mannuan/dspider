# -*- coding:utf-8 -*-

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

class Mongodb(object):
    def __init__(self, db='', collection='', host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    def get_conn(self):
        return MongoClient(host=self.host,port=self.port)

    def get_db(self):
        return Database(self.get_conn(),self.db)

    def get_collection(self):
        return Collection(self.get_db(),self.collection)

    def __str__(self):
        return str({'db':self.get_db(),'collection':self.get_collection(),'host':self.host,'port':self.port})

    def __eq__(self, other):
        if other is None:
            return not self.db or not self.collection
        else:
            return super.__eq__(self,other)
