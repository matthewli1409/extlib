import json
import math

import numpy as np
import pandas as pd
import redis

from extlib.bfx_v2 import BFXV2


class PriceProcessor:

    def __init__(self, insts, df_prices, vol_window, timeframe='1D'):
        """Process price data into standard DataFrame formats

        Arguments:
            insts {list} -- All instruments used for analysis
            df_prices {pandas.DataFrame} -- DataFrame of prices
            vol_window {int} -- Volatility window

        Keyword Arguments:
            timeframe {str} -- '1D', '4H', '1H' etc. (default: {'1D'})
        """
        self.insts = insts
        self.timeframe = timeframe
        self.vol_window = vol_window
        self.df_open = pd.DataFrame()
        self.df_high = pd.DataFrame()
        self.df_low = pd.DataFrame()
        self.df_close = pd.DataFrame()
        self.df_exp_std = pd.DataFrame()
        self.df_rets = pd.DataFrame()
        self.df_std = pd.DataFrame()
        self.df_prices = df_prices
        self.process_open()
        self.process_high()
        self.process_low()
        self.process_close()
        self.process_returns()
        self.process_std()

    def process_close(self):
        """Process closing prices"""
        for inst in self.insts:
            _df = self.df_prices[self.df_prices['coin'] == inst]['close'].rename(inst)
            self.df_close = pd.concat([self.df_close, _df], axis=1, sort=True)
            self.df_close.interpolate(inplace=True)

    def process_high(self):
        """Process high prices"""
        for inst in self.insts:
            _df = self.df_prices[self.df_prices['coin'] == inst]['high'].rename(inst)
            self.df_high = pd.concat([self.df_high, _df], axis=1, sort=True)
            self.df_high.interpolate(inplace=True)

    def process_low(self):
        """Process low prices"""
        for inst in self.insts:
            _df = self.df_prices[self.df_prices['coin'] == inst]['low'].rename(inst)
            self.df_low = pd.concat([self.df_low, _df], axis=1, sort=True)
            self.df_low.interpolate(inplace=True)

    def process_open(self):
        """Process open prices"""
        for inst in self.insts:
            _df = self.df_prices[self.df_prices['coin'] == inst]['open'].rename(inst)
            self.df_open = pd.concat([self.df_open, _df], axis=1, sort=True)
            self.df_open.interpolate(inplace=True)

    def process_returns(self):
        """Process returns"""
        self.df_rets = self.df_close / self.df_close.shift(1) - 1

    def process_std(self):
        """Process standard std and expo. std"""
        self.df_std = self.df_rets.rolling(window=self.vol_window).std() * std_mult(self.timeframe)
        self.df_exp_std = self.df_rets.rolling(window=self.vol_window).apply(
            weighted_expo_std, args=[self.vol_window, self.timeframe], raw=True)


def get_px_hr_redis(insts, rebal_hr, sample=True, host='localhost', port=6379):
    """Get prices from redis

    Arguments:
        insts {list} -- List of instruments to be read from csv
        rebal_hr {list} -- Rebalance hour to filter data for

    Keyword Arguments:
        sample {bool} -- True will return sample prices from redis rather than entire history (default: {True})
        host {string} -- Host of redis (default: {localhost})
        port {int} -- Port of redis (default: {6379})

    Returns:
        pandas.DataFrame -- DataFrame of prices
    """
    df = _get_px_redis(sample=sample, host=host, timeframe='1h')
    df = df[df['coin'].isin(insts)]
    df = df[df.index.hour.isin(rebal_hr)]
    df = df[['open', 'close', 'high', 'low', 'volume', 'coin', 'timeframe']]

    if sample:
        bfx = BFXV2()
        for inst in insts:
            df_price = bfx.get_candles('1h', inst, 'last')
            df_price['timeframe'] = '1h'
            df_price['coin'] = inst
            df_price.columns = map(str.lower, df_price.columns)
            df_price.set_index('ts', inplace=True)
            df = pd.concat([df, df_price], sort=True)
    return df


def _get_px_redis(sample=True, host='localhost', port=6379, timeframe='1h'):
    """Private - Get prices from redis and return

    Keyword Arguments:
        sample {bool} -- True then csv file will be smaller - used for algo trading. Else for backtesting (default: {True})
        host {string} -- Host of redis (default: {localhost})
        port {int} -- Port of redis (default: {6379})
        timeframe {str} -- Timeframe to pull (default: {'1h'})

    Returns:
        pandas.DataFrame -- DataFrame of prices
    """
    r = redis.Redis(host=host)
    filename = f'prices-sample_{timeframe}' if sample else f'prices-all_{timeframe}'
    df = pd.DataFrame(json.loads(r.get(filename)))
    df['dateTime'] = pd.to_datetime(df['dateTime'], unit='ms')
    df.set_index(df['dateTime'], inplace=True)
    return df


def weighted_expo_wgts(std_wind):
    """Calculates the exponential weighting based on the length of the std. window

    Arguments:
        std_wind {int} -- Rolling standard deviation lookback window. This determines how many data points in-between
                            the expo function is needed

    Returns:
        numpy.array -- Exponential weighting between -3 and +3
    """
    x = np.linspace(-3, 3, std_wind)
    upper_func = np.vectorize(lambda t: (1 - math.exp(-t) / 2) + 0.5)
    lower_func = np.vectorize(lambda t: (math.exp(t) / 2) + 0.5)
    upper = x[x >= 0]
    lower = x[x < 0]
    return np.append(lower_func(lower), upper_func(upper))


def weighted_expo_std(df_ret, std_wind, timeframe):
    """Calculates the exponential weighted standard deviation

    Arguments:
        df_ret {pandas.DataFrame} -- DataFrame of returns data
        std_wind {int} -- Rolling standard deviation lookback window. This determines how many points in-between the
                            expo function is needed.
        timeframe {str} -- '1D', '1H' etc. used to annualise the std.

    Returns:
        numpy.array -- Exponetially weighted standard deviation values
    """
    mult_dict = {'1D': 365, '4H': 365 * 8, '1H': 365 * 24}
    expo_wgts = weighted_expo_wgts(std_wind=std_wind)
    weighted_ave = np.sum(df_ret * expo_wgts) / np.sum(expo_wgts)
    return np.sqrt(
        np.sum(np.power(df_ret - weighted_ave, 2) * expo_wgts) / (std_wind - 1)) * math.sqrt(
        mult_dict[timeframe])


def annualise_mult():
    """Returns dictionary of multiplies for annualisation purposes

    Returns:
        dict -- Dictionary of annualisation multiplyers
    """
    return {'1D': 365, '4H': 365 * 6, '1H': 365 * 24}


def std_mult(timeframe):
    """Returns standard deviation multiplier to annualise volatility

    Arguments:
        timeframe {str} -- '1D', '4H', '1H' etc.

    Returns:
        float -- Annualised square root number (365 for daily, 365 * 6 for 4hr timeframe)
    """
    mult = annualise_mult()
    return math.sqrt(mult.get(timeframe))
