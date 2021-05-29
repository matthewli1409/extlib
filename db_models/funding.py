from pymongo.errors import BulkWriteError, DuplicateKeyError

from logger.logger import log_error_msg
from .connect_ryo import get_mongo_client


def funding_db(x, strat_name, bulk=False):
    """Store funding to db

    Arguments:
        x {dict} -- dict of funding to be stored
        strat_name {str} -- name of strat obviously

    Keyword Arguments:
        bulk {bool} -- if bulk, then write in bulk (default: {False})
    """
    mongo_client = get_mongo_client()
    col = mongo_client['funding']
    if bulk:
        try:
            col.insert_many(x)
        except BulkWriteError:
            msg = f'BulkWriteError occurred - saving {strat_name} funding->db'
            log_error_msg(msg)
    else:
        for rec in x:
            try:
                col.insert_one(rec)
            except DuplicateKeyError:
                msg = f'DuplicateKeyError occurred - saving {strat_name} funding->db'
                log_error_msg(msg)


def delete_all_funding_documents():
    """Delete all funding documents, only use this if you know wtf you are doing"""
    mongo_client = get_mongo_client()
    mongo_client['funding'].delete_many({})
