import math

import pandas as pd
from pandas.tseries.offsets import MonthEnd


def annualised_return(tot_ret, days):
    return (1 + tot_ret) ** (365 / days) - 1


def annualised_vol(df_rets, dt_start, dt_end):
    return df_rets.loc[dt_start: dt_end].std() * math.sqrt(365)


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
    df['EOM'] = df.index + MonthEnd(0)
    df.drop_duplicates('EOM', keep='last', inplace=True)
    df = df.loc[df.index == df['EOM']]
    df['M_RETS'] = df['NAV'] / df['NAV'].shift(1) - 1
    df.drop(columns=['EOM', 'NAV'], inplace=True)
    return df.to_json(orient='index')