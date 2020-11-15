from pymongo import MongoClient
from pprint import pprint

def mongo_connect(server_name: str):
    client = MongoClient(server_name)
    db = client.twitter_db
    return db

def mongo_insert(db, data: list, collection_name: str):
    try:
        db[collection_name].insert_many(data)
    except:
        print("Error!")