import pymongo

from .connect_ryo import get_mongo_client


def delete_all_aum_db():
    """Delete all data in aum collection"""
    mongo_client = get_mongo_client()
    col = mongo_client['aum']
    col.delete_many({})


def get_latest_aum_db(fund):
    """Get latest aum of fund from db

    Arguments:
        fund {str} -- Fund to pull aum for

    Returns:
        list -- list of last record recorded in aum by fund
    """
    mongo_client = get_mongo_client()
    return list(mongo_client['aum'].find({'fund': fund}, sort=[('dateTime', pymongo.DESCENDING)]).limit(1))
