import os

import pymongo

from config.settings import MONGODB_DB, STRAT_NAME


def get_mongo_client():
    """Get correct mongo client

    Returns:
        pymongo.database.Database -- client that points to db
    """
    mongo_client = pymongo.MongoClient(os.environ['MONGODB_CLIENT'])
    return mongo_client[MONGODB_DB]


def get_strat_info_db(strat, mongo_client=None):
    """Get strat information

    Arguments:
        strat {str} -- strategy name "MA_BO_I"

    Keyword Arguments:
        mongo_client {client} -- use user provided mongo client else function will call itself (default: {None})

    Returns:
        list -- list of strat information
    """
    if mongo_client is None:
        mongo_client = get_mongo_client()
    return list(mongo_client['settings'].find({'strategy': strat}))[0]


def get_last_run():
    """Get last time the strategy was ran

    Returns:
        datetime.datetime -- datetime of the last time the strat was ran
    """
    strat_info = get_strat_info_db(STRAT_NAME)
    return strat_info.get('lastRun')


def set_last_run(dt):
    """Get last time the strategy was ran

    Arguments:
        dt {datetime.datetime} -- datetime to set
    """
    mongo_client = get_mongo_client()
    query = {'strategy': STRAT_NAME}
    newvalues = {'$set': {'lastRun': dt}}
    mongo_client['settings'].update_one(query, newvalues)
