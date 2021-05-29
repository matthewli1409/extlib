import pandas as pd
from dateutil import parser
from pymongo.errors import BulkWriteError

from logger.logger import log_error_msg
from .connect_ryo import get_mongo_client


def get_trades_db_by_dt(strat, date_st, date_end):
    """Get all trades from specific strategy

    Args:
        strat (str): strategy name
        date_st (datetime.datetime): start date
        date_end (datetime.datetime): end date
    """
    mongo_client = get_mongo_client()
    query = {"strat": strat, "dateTime": {"$gte": date_st, "$lte": date_end}}
    return pd.DataFrame((list(mongo_client['trades'].find(query))))


def get_all_trades_db(strat):
    """Get all trades from specific strategy

    Args:
        strat (str): strategy name
    """
    mongo_client = get_mongo_client()
    return pd.DataFrame((list(mongo_client['trades'].find({'strat': strat}))))


def delete_all_strat_trades(strat):
    """Delete all trades from a strat

    Arguments:
        strat_name {str} - 'MA_BO_I', 'NAX_TREND' etc.
    """
    mongo_client = get_mongo_client()
    mongo_client['trades'].delete_many({'strat': strat})


def delete_trades_by_dt(strat, date_start, date_end):
    """Delete trades from a strat

    Arguments:
        strat_name {str} - 'MA_BO_I', 'NAX_TREND' etc.
        date_start {str} - date to delete from in string format
        date_end {str} - date to end delete in string format
    """
    mongo_client = get_mongo_client()
    query = {"strat": strat, "dateTime": {"$gte": parser.parse(date_start), "$lte": parser.parse(date_end)}}
    x = mongo_client['trades'].delete_many(query)
    print(f'{x.deleted_count} trades deleted for {strat}')


def trades_to_db(x, strat_name):
    """Store trades to db

    Arguments:
        x {dict} -- dict of funding to be stored
        strat_name {str} -- name of strat obviously
    """
    mongo_client = get_mongo_client()
    col = mongo_client['trades']
    try:
        col.insert_many(x)
    except BulkWriteError:
        msg = f'BulkWriteError occurred - saving {strat_name} funding->db'
        log_error_msg(msg)
