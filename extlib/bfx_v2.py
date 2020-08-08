import hashlib
import hmac
import json
import time

import numpy as np
import pandas as pd
import requests


class BFXV2:

    def __init__(self, key=None, secret=None):
        """BFX V2 REST Public and Authenticated endpoints

        Keyword Arguments:
            key {str} -- api key generated from BFX (default: {None})
            secret {str} -- api secret generated from BFX (default: {None})
        """
        self.url = 'https://api.bitfinex.com/'
        self.key = key
        self.secret = secret

    @staticmethod
    def _get_nonce():
        """Get a unique nonce based on time

        Returns:
            str -- A nonce based on current time
        """
        return str(int(round(time.time() * 10000)))

    def _get_headers(self, body, path):
        """Get headers for authenticated endpoints

        Arguments:
            body {JSON} -- Optional parameters sent through request in JSON format
            path {str} --  Path of request (i.e. "v2/auth/r/int/report")

        Returns:
            dict -- Header dictionary for authenticated endpoint request
        """
        nonce = self._get_nonce()
        secbytes = self.secret.encode(encoding='UTF-8')
        signature = '/api/' + path + nonce + body
        sigbytes = signature.encode(encoding='UTF-8')
        h = hmac.new(secbytes, sigbytes, hashlib.sha384)
        hexstring = h.hexdigest()
        return {
            'bfx-nonce': nonce,
            'bfx-apikey': self.key,
            'bfx-signature': hexstring,
            'content-type': 'application/json'
        }

    def _req(self, path, params=None):
        """Get headers for authenticated endpoints

        Arguments:
            path {str} -- Path of request (i.e. "v2/auth/r/int/report")

        Keyword Arguments:
            params {dict} -- Option parameters sent through request (default: {None})

        Returns:
            requests.models.Response -- Data that is requested in JSON format
        """
        params = params if params else {}
        raw_body = json.dumps(params)
        headers = self._get_headers(raw_body, path)
        url = self.url + path
        resp = requests.post(url, headers=headers, data=raw_body, verify=True)
        return resp

    def get_oi(self, symbol):
        """Get open interest of a symbol

        Arguments:
            symbol {str} -- Symbol for the OI

        Returns:
            list -- [[timestamp, long_oi], [timestamp, short_oi]]
        """
        oi = []
        for side in ['long', 'short']:
            extension = f'v2/stats1/pos.size:1m:t{symbol}:{side}/last'
            res = requests.get(self.url + extension)
            oi.append(res.json())
        return oi

    def get_margin_inst(self):
        """Get a list of list of margin instruments

        Returns:
            list -- ['BABBTC', 'BABUSD', 'BSVBTC' ...]]
        """
        extension = f'v2/conf/pub:list:pair:margin'
        res = requests.get(self.url + extension)
        return res.json()[0]

    def get_exchange_inst(self):
        """Get a list of exchanged traded instruments

        Returns:
            list -- ['BABBTC', 'BABUSD', 'BSVBTC' ...]
        """
        extension = f'v2/conf/pub:list:pair:exchange'
        res = requests.get(self.url + extension, timeout=10)
        return res.json()

    def get_margin_info(self, key):
        """Get account margin information (like P/L, Swaps, Margin Balance, Tradable Balance and others).
            Use different keys (base, SYMBOL, sym_all) to retrieve different kinds of data.

        Notes:
            - https://api.bitfinex.com/v2/auth/r/info/margin/base

        Arguments:
            key {str} -- "base" | "SYMBOL" | sym_all

        Returns:
            [json] -- [PnL, Swap, Margin_Balance, 'Margin_Net, Margin_Min, Tradable_Bal, Gross_Balance]
        """
        res = self._req(f'v2/auth/r/info/margin/base')
        return res.json()

    def get_trade_ticker_info(self, coin='ALL'):
        """Method to pull Trade Ticker Info from BFX. Contains the following columns:
                ['SYMBOL', 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_PERC', 'PX_LAST', 'VOLUME', 'HIGH', 'LOW'

        Keyword Arguments:
            coin {str} -- 'All' or individual names (i.e. tBTCUSD) (default: {'ALL'})

        Returns:
            pandas.DataFrame -- DataFrame of required trade ticker
        """
        extension = 'v2/tickers?symbols={}'.format(coin)
        res = requests.get(self.url + extension)
        trade_cols = ['SYMBOL', 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_PERC',
                      'PX_LAST', 'VOLUME', 'HIGH', 'LOW']
        trade_data = (x for x in res.json() if x[0].startswith('t'))
        df_tickers = pd.DataFrame(trade_data, columns=trade_cols)

        df_tickers['LLEG'] = np.where(df_tickers['SYMBOL'].str.contains(':'),
                                      df_tickers['SYMBOL'].str.split(':').str[0].str[1:],
                                      df_tickers['SYMBOL'].str[1:4])

        df_tickers['RLEG'] = np.where(df_tickers['SYMBOL'].str.contains(':'),
                                      df_tickers['SYMBOL'].str.split(':').str[1],
                                      df_tickers['SYMBOL'].str[-3:])
        return df_tickers

    def get_bfx_fx(self, ccy1, ccy2):
        """Calls BFX FX API to get current FX rate]

        Arguments:
            ccy1 {str} -- FX left leg
            ccy2 {str} -- FX right leg

        Returns:
            dict -- {'RLEG': 'EUR', 'RATE': 1.13971154}
        """
        extension = 'v2/calc/fx'
        params = {'ccy1': ccy1, 'ccy2': ccy2}
        res = requests.post(self.url + extension, params=params)

        fx_rate = res.json()
        output = {'LLEG': ccy1, 'RLEG': ccy2, 'FX_RATE': fx_rate[0]}
        return output

    def get_candles(self, freq, coin, section, start=None, end=None, limit=20, sort=-1):
        """Calls BFX candles API to get candle data OHLCV

        Arguments:
            freq {str} -- Available values: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M'
            coin {str} --  The symbol you want information about. (tBTCUSD)
            section {str} -- Available values: "last", "hist

        Keyword Arguments:
            start {int} -- ms start time for candle (default: {None})
            end {int} -- ms end time for candles (default: {None})
            limit {int} -- Number of candles requested (max: 5000) (default: {20})
            sort {int} -- If = 1 it sorts results returned with old > new (default: {-1})

        Returns:
            pandas.DataFrame -- DataFrame of candles
        """
        extension = f'v2/candles/trade:{freq}:{coin}/{section}'
        params = {'limit': limit, 'sort': sort, 'start': start, 'end': end}
        res = requests.get(self.url + extension, params=params, timeout=10)

        if not res.status_code == 500:
            # If data is 'last' then wrap it in a list to keep list in row format in DataFrame
            data = res.json() if section == 'hist' else [res.json()]
            df = pd.DataFrame(data)
            df.rename(columns=dict(zip(df.columns, ['TS', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME'])), inplace=True)
            df['TS'] = pd.to_datetime(df['TS'], unit='ms')
            df.sort_values('TS', inplace=True)
            return df

    def get_wallets(self, wallet_type='all'):
        """Get personal wallets from BFX (Margin, Exchange, Credit-line)

        Keyword Arguments:
            wallet_type {str} -- 'all'/'margin'/'exchange' etc. (default: {'all'})

        Returns:
            pandas.DataFrame -- DataFrame of wallets
        """
        res = self._req(f'v2/auth/r/wallets')
        df = pd.DataFrame(res.json())
        df.rename(columns=dict(zip(df.columns, ['WALLET_TYPE', 'CURRENCY', 'BALANCE',
                                                'UNSETTLED_INTEREST', 'BALANCE_AVAILABLE', '1', '2'])), inplace=True)

        if wallet_type != 'all':
            df = df[df['WALLET_TYPE'] == wallet_type]

        # Compute dollar value for the wallet
        df_tickers = self.get_trade_ticker_info()
        df_tickers = df_tickers[df_tickers['RLEG'] == 'USD']
        df = df.merge(df_tickers[['LLEG', 'PX_LAST']], how='left', left_on='CURRENCY', right_on='LLEG')
        df.loc[df['CURRENCY'] == 'USD', 'PX_LAST'] = 1
        df['USD_VAL'] = df['BALANCE'].mul(df['PX_LAST'])
        return df

    def get_positions(self, adjusted_pnl=False):
        """Get personal positions from BFX

        Keyword Arguments:
            adjusted_pnl {bool} --  True then get current ticker price and compute PnL manually as BFX takes exit fees into account (default: {False})

        Returns:
            pandas.DataFrame -- DataFrame of positions
        """
        try:
            res = self._req(f'v2/auth/r/positions')
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            return f'Error: {err}'

        df = pd.DataFrame(res.json())
        df.rename(
            columns=dict(zip(df.columns, ['INST', 'STATUS', 'AMOUNT', 'BASE_PRICE', 'FUNDING', 'FUNDING_TYPE', 'PNL'])), inplace=True)

        if adjusted_pnl:
            df_tickers = self.get_trade_ticker_info()
            df = pd.merge(df, df_tickers[['SYMBOL', 'PX_LAST']], how='left', left_on='INST', right_on='SYMBOL')
            df['ADJUSTED_PNL'] = (df['PX_LAST'] - df['BASE_PRICE']) * df['AMOUNT']

        return df

    def get_ledgers(self, ccy, start, end, category, limit=500):
        """Get ledgers

        Arguments:
            ccy {str} -- 'USD', 'BTC', 'ETH' etc.
            start {int} -- ms start time
            end {int} -- ms end time
            category {int} -- 201 for Trading fees/31 for settlement fees/22 for positions closed

        Keyword Arguments:
            limit {int} -- The max number of records to pull (default: {500})

        Returns:
            pandas.DataFrame -- DataFrame of ledger entries
        """
        params = {'limit': limit, 'start': start, 'end': end, 'category': category}
        res = self._req(f'v2/auth/r/ledgers/{ccy}/hist', params=params)

        df = pd.DataFrame(res.json())
        df.rename(
            columns=dict(zip(df.columns, ['ID', 'CCY', '', 'TS', '', 'AMOUNT', 'BALANCE', '', 'DESC'])),
            inplace=True)
        df['TS'] = pd.to_datetime(df['TS'], unit='ms')
        return df

    def get_trades(self, start, end, limit=1000, sort=-1):
        """Get trades

        Arguments:
            start {int} -- ms start time
            end {int} -- ms end time

        Keyword Arguments:
            limit {int} -- The max number of records to pull (default: {1000})
            sort {int} -- If -1 it sorts results return with old > new (default: {-1})

        Returns:
            pandas.DataFrame -- DataFrame of trades
        """
        params = {'limit': limit, 'start': start, 'end': end}
        res = self._req(f"v2/auth/r/trades/hist", params=params)

        df = pd.DataFrame(res.json())
        df.rename(columns=dict(zip(df.columns, ['ID', 'PAIR', 'TS', 'ORDER_ID', 'AMOUNT',
                                                'PRICE', 'TYPE', 'ORDER_PRICE', 'MAKER', 'FEE', 'FEE_CCY'])), inplace=True)
        df['TS'] = pd.to_datetime(df['TS'], unit='ms')
        return df

    def get_margin_config(self):
        """Get margin config from BFX

        Returns:
            pandas.DataFrame -- DataFrame margin and risk coefficients (1 - haircut)
        """
        extension = f'v2/conf/pub:spec:margin'
        res = requests.get(self.url + extension, timeout=10)

        data = res.json()[0]
        haircut_dict = data.get('conf')
        initial_dict = data.get('initial')
        mm_dict = data.get('minimum')

        df_riskcoeff = pd.DataFrame(list(haircut_dict.items()), columns=['COIN', 'RISKCOEFF'])
        del_rows = ['base_size_thres', 'base_size_incr', 'base_step', 'base_haircut']
        df_riskcoeff = df_riskcoeff[~df_riskcoeff['COIN'].isin(del_rows)]
        df_riskcoeff['COIN'] = df_riskcoeff['COIN'].str[:3]

        df_initial = pd.DataFrame(list(initial_dict.items()), columns=['SYMBOL', 'INITIAL_MARGIN'])
        df_maintenance = pd.DataFrame(list(mm_dict.items()), columns=['SYMBOL', 'MAINTENANCE_MARGIN'])
        del_rows = ['base', 'base_cap']

        df_margin = pd.merge(df_initial, df_maintenance, how='left', left_on='SYMBOL', right_on='SYMBOL')
        df_margin = df_margin[~df_margin['SYMBOL'].isin(del_rows)]

        return df_margin, df_riskcoeff

    def get_order_books(self, symbol, precision='P0', depth=100):
        """Get order book from BFX

        Arguments:
            symbol {str} -- 'tBTCUSD'

        Keyword Arguments:
            precision {str} -- Level of price aggregation (P0, P1, P2, P3, P4, R0) (default: {'P0'})
            depth {int} -- Depth of book wanted (default: {100})

        Returns:
            pandas.DataFrame -- DataFrame of bid and ask books
        """
        extension = f'v2/book/{symbol}/{precision}'
        params = {'len': depth}
        res = requests.get(self.url + extension, params=params, timeout=10)

        df = pd.DataFrame(res.json(), columns=['PRICE', 'COUNT', 'AMOUNT'])
        df_bid = df[df['AMOUNT'] > 0].copy()
        df_bid['ABS_CUMULATIVE_AMOUNT'] = abs(df_bid['AMOUNT'].cumsum())
        df_offer = df[df['AMOUNT'] < 0].copy()
        df_offer['ABS_CUMULATIVE_AMOUNT'] = abs(df_offer['AMOUNT'].cumsum())
        return df_bid, df_offer

    def get_aum(self):
        """Returns the aum of your margin account

        Returns:
            float -- how much dough you have duh
        """
        df_cur_pos = self.get_positions(adjusted_pnl=True)
        df_margin_wallet = self.get_wallets('margin')

        gross_aum = df_margin_wallet['USD_VAL'].sum()
        pnl = df_cur_pos['ADJUSTED_PNL'].sum()
        aum = gross_aum + pnl
        return aum

    def get_cur_pos(self):
        """Returns live positions currently on margin

        Returns:
            list -- list of dictionary of positions
        """
        df_cur_pos = self.get_positions(adjusted_pnl=True)
        if len(df_cur_pos.index) == 0:
            cur_pos = {}
        else:
            df_cur_pos = df_cur_pos[['INST', 'AMOUNT', 'BASE_PRICE', 'FUNDING', 'ADJUSTED_PNL', 'PX_LAST']]
            df_cur_pos.columns = map(str.lower, df_cur_pos.columns)
            df_cur_pos.rename(columns={'amount': 'cur_lots'}, inplace=True)
            cur_pos = df_cur_pos[['inst', 'cur_lots', 'adjusted_pnl', 'funding', 'px_last']].to_dict('records')

            for inst in cur_pos:
                inst['$_exposure'] = inst['cur_lots'] * inst['px_last']
        return cur_pos
