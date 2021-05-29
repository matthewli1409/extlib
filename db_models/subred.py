import pandas as pd

from .connect_ryo import get_mongo_client


def get_subred_db(strat):
    """Get all subred from specific strategy

    Arguments:
        strat (str): strategy name
    """
    mongo_client = get_mongo_client()
    return pd.DataFrame((list(mongo_client['subred'].find({'strat': strat}))))
