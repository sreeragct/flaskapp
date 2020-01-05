import pymongo


class Database(object):
    @staticmethod
    def initialize():
        client = pymongo.MongoClient("mongodb+srv://Test:Test123@cluster0-1n9p4.mongodb.net/test?retryWrites=true&w=majority")
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