from .connect_ryo import get_mongo_client


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
