import pymongo
import os


def get_mongo_client():
    """Get correct mongo client

    Returns:
        pymongo.database.Database -- client that points to db
    """
    mongo_client = pymongo.MongoClient(os.environ['MONGODB_CLIENT'])
    return mongo_client[os.environ['RYO_DB']]
