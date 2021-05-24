from db_models.connect_ryo import get_mongo_client


def bt_perf_db(record):
    """Save a backtest document to collection

    Arguments:
        record {dict} -- record to be record to collection
    """
    mongo_client = get_mongo_client()
    col = mongo_client['backtest']
    col.insert(record)


def get_bt_db(strat):
    """Get backtest results from backtest collection

    Arguments:
        strat {str} -- strategy name "MA_BREAKOUT_I"
    """
    mongo_client = get_mongo_client()
    col = mongo_client['backtest']
    res = list(col.find({'strat': strat}))
    return res
