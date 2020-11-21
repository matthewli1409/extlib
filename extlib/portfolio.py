import math

import pandas as pd
from pandas.tseries.offsets import MonthEnd


def get_tf_multiplier():
    """Returns timeframe multiplier"""
    return {'1D': 1, '4H': 6, '1H': 24}


def annualised_return(tot_ret, periods, timeframe='1D'):
    """Returns annualised returns"""
    tf_multiplier = get_tf_multiplier()
    return (1 + tot_ret) ** ((365 * tf_multiplier.get(timeframe)) / periods) - 1


def annualised_vol(df_rets, dt_start, dt_end, timeframe='1D'):
    """Returns annualised vol"""
    tf_multiplier = get_tf_multiplier()
    return df_rets.loc[dt_start: dt_end].std() * math.sqrt(365 * tf_multiplier.get(timeframe))


def sharpe_ratio(ann_ret, ann_vol):
    return ann_ret / ann_vol


def get_df_hwm(df_nav):
    return df_nav.cummax()


def high_water_mark(df_nav):
    return get_df_hwm(df_nav).max()


def get_df_dd(df_nav):
    return df_nav / get_df_hwm(df_nav) - 1


def max_drawdown(df_nav):
    return get_df_dd(df_nav).min()


def total_tx(df_tx, dt_start, dt_end):
    return df_tx[dt_start: dt_end].sum()


def perf_per_month(df):
    """Returns monthly performance of strategy

    Arguments:
        df {pandas.Series} -- Series of NAV with datetime as the index

    Returns:
        json -- Monthly returns and datetime as the index
    """
    df = df.to_frame()
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")
    df['eom'] = df.index + MonthEnd(0)
    df.drop_duplicates('eom', keep='last', inplace=True)
    df = df.loc[df.index == df['eom']]
    df['m_rets'] = df['nav'] / df['nav'].shift(1) - 1
    df.drop(columns=['eom', 'nav'], inplace=True)
    return df.to_json(orient='index')
