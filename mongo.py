from pymongo import MongoClient

DATABSE_URL = "mongodb://localhost:27017"

def get_mongo_client():
    return MongoClient(DATABSE_URL)