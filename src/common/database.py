import os
import pymongo

class Database():
    URI = os.environ.get("MONGOLAB_URL")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['webapp']
    
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
    
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)
    
    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
