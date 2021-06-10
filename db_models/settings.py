from .connect_ryo import get_mongo_client


def get_fund_info_db(fund):
    """Get fund information

    Arguments:
        fund {str} -- fund name "MASTER_FUND"

    Returns:
        list -- list of fund information
    """
    mongo_client = get_mongo_client()
    return list(mongo_client['settings'].find({'fund': fund}))[0]


def get_strat_info_db(strat):
    """Get strat information

    Arguments:
        strat {str} -- strategy name "MA_BO_I"

    Keyword Arguments:
        mongo_client {client} -- use user provided mongo client else function will call itself (default: {None})

    Returns:
        list -- list of strat information
    """
    mongo_client = get_mongo_client()
    return list(mongo_client['settings'].find({'strategy': strat}))[0]


def get_all_strats_db():
    """Get all strats that exist in the settings collection

    Returns:
        list -- list of documents that have key: 'STRAT_INFO'
    """
    mongo_client = get_mongo_client()
    return list(mongo_client['settings'].find({'key': 'STRAT_INFO'}))


def get_last_run_db(strat):
    """Get last time the strategy was ran

    Returns:
        datetime.datetime -- datetime of the last time the strat was ran
    """
    strat_info = get_strat_info_db(strat)
    return strat_info.get('lastRun')


def set_last_run_db(strat, dt):
    """Get last time the strategy was ran

    Arguments:
        dt {datetime.datetime} -- datetime to set
    """
    mongo_client = get_mongo_client()
    query = {'strategy': strat}
    newvalues = {'$set': {'lastRun': dt}}
    mongo_client['settings'].update_one(query, newvalues)


def get_haircut_db(strat_name):
    """Get haircut from db

    Arguments:
        strat_name {str} -- strategy to get haircut for

    Returns:
        float -- haircut value from db
    """
    strat_info = get_strat_info_db(strat_name)
    return strat_info.get('haircut', 0)


def get_public_puller_info():
    """Get public puller instruments"""
    mongo_client = get_mongo_client()
    query = {'key': 'PUBLIC_PULLER'}
    return list(mongo_client['settings'].find(query))[0]
