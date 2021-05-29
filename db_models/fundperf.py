from pymongo.errors import BulkWriteError

from logger.logger import log_generic_msg, log_error_msg
from .connect_ryo import get_mongo_client


def perf_db(records, save_all_data=False, fund=''):
    """Save LIVE ACTUAL performance of fund to database

    Keyword Arguments:
        save_all_data {bool} -- if False then only saves data that does not exist in db (default: {False})
        records {dict} -- dictionary of all records to be saved to fundperf collection
        fund {str} -- if override is required for fund name that is originally a environment variable
    """
    mongo_client = get_mongo_client()
    col = mongo_client['fundperf']
    col.delete_many({'fund': fund})

    try:
        log_generic_msg(f'Last fundperf document to be recorded: {records[-1]}')
        col.insert_many(records)
        log_generic_msg(f'{fund} actual performance successfully recorded')
    except BulkWriteError as bwe:
        log_error_msg(bwe.details)
