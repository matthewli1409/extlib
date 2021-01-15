import pandas as pd
import requests


class Bin:

    def __init__(self):
        """Binance exchange REST API"""
        self.base_url = 'https://api.binance.com/api/'

    def get_candles(self, coin, freq):
        """Get historical candles

        Arguments:
            coin {str} -- coin to pull candle data for (btc-usd)
            start {datetime} -- date to start data pull for in iso 8601 format
            end {datetime} -- date to end data pull for in iso 8601 format

        Returns:
            pandas.DataFrame -- DataFrame of candles
        """
        extension = f'v1/klines'
        params = {'symbol': coin, 'interval': freq}
        res = requests.get(self.base_url + extension, params=params, timeout=10)
        df = pd.DataFrame(res.json())
        df.rename(columns=dict(zip(df.columns, ['TS', 'LOW', 'HIGH', 'OPEN', 'CLOSE', 'VOLUME'])), inplace=True)
        df['TS'] = pd.to_datetime(df['TS'], unit='ms')
        df.sort_values('TS', inplace=True)
        return df


def get_candles_example():
    """Simple example to get candle data from api"""
    Bin().get_candles('BTCUSDT', '1d')
