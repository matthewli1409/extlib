import pymongo


class ConnectMongoDB:
    def __init__(self, db, client):
        self.client = client
        self.db = db

    def get_mongo_client(self):
        """Get correct mongo client

        Returns:
            pymongo.database.Database -- client that points to db
        """
        mongo_client = pymongo.MongoClient(self.client)
        return mongo_client[self.db]
