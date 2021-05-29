import pandas as pd
import pymongo

from .connect_ryo import get_mongo_client


def balance_db(x):
    """Store balance to db

    Arguments:
        x {dict} -- dictionary of balances to be stored
    """
    mongo_client = get_mongo_client()
    col = mongo_client['balances']
    col.insert_one(x)


def get_latest_balances_db(strat):
    """Get latest performance from modelperf collection

    Arguments:
        strat {str} -- Strat to pull from modelperf collection

    Returns:
        list -- list of last record recorded in modelperf by strategy
    """
    mongo_client = get_mongo_client()
    return list(mongo_client['balances'].find({'strat': strat}, sort=[('dateTime', pymongo.DESCENDING)]).limit(1))


def get_balances_eod_db(date_st, date_end, strat):
    """Get balances at the end of the day only

    Arguments:
        date_st {datetime} --  start date
        date_end {datetime} -- end date
        strat {str} -- strategy to pull balances for in the collection

    Returns:
        pd.DataFrame --  aum, dateTime, strat
    """
    date_st = date_st.replace(hour=23, minute=59, second=0)
    date_end = date_end.replace(hour=23, minute=59, second=59)
    query = [
        {
            "$match": {
                "dateTime": {
                    "$gte": date_st,
                    "$lte": date_end,
                },
                "strat": strat
            }
        },
        {
            "$addFields": {
                "year": {
                    "$year": "$dateTime"
                },
                "month": {
                    "$month": "$dateTime"
                },
                "day": {
                    "$dayOfMonth": "$dateTime"
                },
            },
        },
        {
            "$sort": {
                "dateTime": -1
            }
        },
        {
            "$group": {
                "_id": {
                    "year": "$year",
                    "month": "$month",
                    "day": "$day",
                },
                "data": {
                    "$first": "$$ROOT"
                }
            }
        },
    ]
    mongo_client = get_mongo_client()
    data = mongo_client['balances'].aggregate(query)

    bal = []
    prices = []
    for x in data:
        bal.append(x.get('data'))
    df_balances = pd.DataFrame(bal)
    df_balances.sort_values('dateTime', inplace=True)
    return df_balances
