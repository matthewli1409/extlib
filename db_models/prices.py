from .connect_ryo import get_mongo_client
import pandas as pd


def get_prices_eod_db(date_st, date_end):
    """Get prices at the end of the day only

    Arguments:
        date_st (datetime.datetime): start date
        date_end (datetime.datetime): end date
    """
    date_st = date_st.replace(hour=23, minute=44, second=50)
    date_end = date_end.replace(hour=23, minute=59, second=59)
    query = [
        {
            "$match": {
                "dateTime": {
                    "$gte": date_st,
                    "$lte": date_end
                },
                "timeframe": '1h'
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
                    "coin": "$coin"
                },
                "data": {
                    "$first": "$$ROOT"
                }
            }
        },
    ]
    mongo_client = get_mongo_client()
    data = mongo_client['prices'].aggregate(query)

    df_data = []
    for x in data:
        df_data.append(x.get('data'))
    df = pd.DataFrame(df_data)
    df.sort_values('dateTime', inplace=True)
    return df
