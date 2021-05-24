import pymongo

from settings import MONGO_DB, MONGO_CLIENT


def get_mongo_client():
    """Get correct mongo client

    Returns:
        pymongo.database.Database -- client that points to db
    """
    mongo_client = pymongo.MongoClient(MONGO_CLIENT)
    return mongo_client[MONGO_DB]
