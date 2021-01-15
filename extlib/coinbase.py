from datetime import datetime

import pandas as pd
import requests


class CoinBase:

    def __init__(self):
        """Coinbase exchange REST API"""
        self.base_url = 'https://api.pro.coinbase.com/'

    def get_candles(self, coin, start, end):
        """Get historical candles

        Arguments:
            coin {str} -- coin to pull candle data for (btc-usd)
            start {datetime} -- date to start data pull for in iso 8601 format
            end {datetime} -- date to end data pull for in iso 8601 format

        Returns:
            pandas.DataFrame -- DataFrame of candles
        """
        extension = f'products/{coin}/candles'
        params = {'start': start, 'end': end, 'granularity': 86400}
        res = requests.get(self.base_url + extension, params=params, timeout=10)
        df = pd.DataFrame(res.json())
        df.rename(columns=dict(zip(df.columns, ['TS', 'LOW', 'HIGH', 'OPEN', 'CLOSE', 'VOLUME'])), inplace=True)
        df['TS'] = pd.to_datetime(df['TS'], unit='s')
        df.sort_values('TS', inplace=True)
        return df


def get_candles_example():
    """Simple example to get candle data from api"""
    start = datetime(2020, 6, 2).isoformat()
    end = datetime(2021, 2, 1).isoformat()
    df = CoinBase().get_candles('btc-usd', start, end)
