import pymongo


class Database(object):
    @staticmethod
    def initialize():
        client = pymongo.MongoClient("mongodb://Test:Test123@ds157624.mlab.com:57624/heroku_jzzwnszb")
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
