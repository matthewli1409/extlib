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
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S").date
    df['eom'] = df.index + MonthEnd(0)
    df.drop_duplicates('eom', keep='last', inplace=True)
    df = df.loc[df.index == df['eom']]
    df['m_rets'] = df['nav'] / df['nav'].shift(1) - 1
    df.drop(columns=['eom', 'nav'], inplace=True)
    return df.to_json(orient='index')


def get_daily_stats(df):
    """Returns daily stats of strategy

    Arguments:
        df {pandas.Series} -- Series of NAV with datetime as the index

    Returns:
        dict -- dictionary of daily stats
    """
    df = df.to_frame()
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S").date
    df = df[~df.index.duplicated(keep='last')]
    df['nav_diff'] = df['nav'] - df['nav'].shift(1)

    no_updays = len(df[df['nav_diff'] > 0])
    no_downdays = len(df[df['nav_diff'] < 0])
    win_loss_day_ratio = no_updays / no_downdays
    ave_updays = df[df['nav_diff'] > 0]['nav_diff'].mean()
    ave_downdays = df[df['nav_diff'] < 0]['nav_diff'].mean()
    max_upday = df[df['nav_diff'] > 0]['nav_diff'].max()
    max_downday = df[df['nav_diff'] < 0]['nav_diff'].min()

    return {'no_updays': no_updays,
            'no_downdays': no_downdays,
            'win_loss_day_ratio': win_loss_day_ratio,
            'ave_updays': ave_updays,
            'ave_downdays': ave_downdays,
            'max_upday': max_upday,
            'max_downday': max_downday,
            }
