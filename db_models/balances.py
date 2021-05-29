from .connect_ryo import get_mongo_client


def balance_db(x):
    """Store balance to db

    Arguments:
        x {dict} -- dictionary of balances to be stored
    """
    mongo_client = get_mongo_client()
    col = mongo_client['balances']
    col.insert_one(x)
