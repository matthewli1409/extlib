import pandas as pd
import pymongo
from pymongo.errors import DuplicateKeyError, BulkWriteError

from logger.logger import log_generic_msg, log_error_msg
from .connect_ryo import get_mongo_client


def model_perf_db(df, strat, save_all_data=False):
    """Save model performance to mongodb

    Arguments:
        df {pandas.DataFrame} -- columns - dateTime, model, rets
        strat {str} -- strategy name
        save_all_data {bool}

    Keyword Arguments:
        save_all_data {bool} -- Will save all DataFrame info if true, else only the ones after latest (default: {False})
    """
    mongo_client = get_mongo_client()
    col = mongo_client['modelperf']

    # Save everything in DataFrame one by one - use this to ensure all records are complete but will be slow
    if save_all_data:
        for record in df.to_dict('records'):
            try:
                col.insert_one(record)
            except DuplicateKeyError as err:
                log_error_msg(err)
        log_generic_msg(f'Completed saving {strat} performance to db - all data')

    # Find latest dateTime save in mongo and only save records after that date
    else:
        df_db = pd.DataFrame(list(col.find({'strat': strat})))

        if not df_db.empty:
            df_db.sort_values('dateTime', inplace=True)
            latest = df_db['dateTime'].iloc[-1]
            records = df[df['dateTime'] > latest][['dateTime', 'rets', 'strat']].to_dict('records')
        else:
            records = df.to_dict('records')

        if len(records) > 0:
            try:
                col.insert_many(records)
            except BulkWriteError as bwe:
                log_error_msg(bwe.details)
        log_generic_msg(f'Completed saving {strat} performance to db - partial data')


def get_model_perf_db(strats):
    """Get model performance from a list of strategies provided from modelperf collection

    Arguments:
        strats {list} -- list of strategies ['MA_BO', 'MAX_TREND']

    Returns:
        list -- list of performance from modelperf collection
    """
    mongo_client = get_mongo_client()
    query = {'strat': {'$in': strats}}
    return list(mongo_client['modelperf'].find(query))


def get_latest_modelperf_db(strat):
    """Get latest performance from modelperf collection

    Arguments:
        strat {str} -- Strat to pull from modelperf collection

    Returns:
        list -- list of last record recorded in modelperf by strategy
    """
    mongo_client = get_mongo_client()
    return list(mongo_client['modelperf'].find({'strat': strat}, sort=[('dateTime', pymongo.DESCENDING)]).limit(1))


def delete_all_model_perf_db(strat):
    """Delete all data in modelperf collection"""
    mongo_client = get_mongo_client()
    col = mongo_client['modelperf']
    col.delete_many({'strat': strat})
