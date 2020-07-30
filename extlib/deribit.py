import time

import pandas as pd
import requests


class Deribit():

    def __init__(self):
        """Deribit exchange REST API"""
        self.base_url = 'https://deribit.com/api/v2/'

    def get_all_insts_data(self, instruments, type='option'):
        """Get all instruments traded on the exchange

        Arguments:
            instruments {list} -- List of instruments ['BTC', 'ETH']

        Keyword Arguments:
            type {str} -- 'option' or 'future' (default: {'option'})

        Returns:
            pandas.DataFrame -- DataFrame of instruments
                Index: ['tick_size', 'taker_commission', 'strike', 'settlement_period',
                        'quote_currency', 'option_type', 'min_trade_amount', 'maker_commission',
                        'kind', 'is_active', 'instrument_name', 'expiration_timestamp',
                        'creation_timestamp', 'contract_size', 'base_currency', 'expiration', 'mste', 'ste', 'dte']
        """
        df_data = pd.DataFrame()
        for coin in instruments:
            r = requests.get(f'{self.base_url}public/get_instruments?currency={coin}&kind={type}&expired=false')
            df = pd.DataFrame(r.json()['result'])
            df['expiration'] = pd.to_datetime(df['expiration_timestamp'], unit='ms')
            df['mste'] = df['expiration_timestamp'] - time.time() * 1000
            df['ste'] = df['mste'] / 1000
            df['dte'] = df['ste'] / 86400
            df_data = pd.concat([df_data, df])
        return df_data

    def get_inst_summary(self, instrument):
        """Get instrument summary

        Arguments:
            instrument {str} -- i.e. 'BTC-22MAY20-9250-P'

        Returns:
            dict -- Instrument data, keys include:
                ['underlying_price', 'underlying_index', 'timestamp', 'stats', 'state', 'settlement_price',
                'open_interest', 'min_price', 'max_price', 'mark_price', 'mark_iv', 'last_price',
                'interest_rate', 'instrument_name', 'index_price', 'greeks', 'estimated_delivery_price',
                'change_id', 'bids', 'bid_iv', 'best_bid_price', 'best_bid_amount', 'best_ask_price',
                'best_ask_amount', 'asks', 'ask_iv']
        """
        r = requests.get(f'{self.base_url}public/get_order_book?depth=5&instrument_name={instrument}')
        return r.json()['result']

    def get_order_book(self, instrument):
        """Get order book

        Arguments:
            instrument {str} -- i.e. 'BTC-22MAY20-9250-C'

        Returns:
            json -- Response includdes bids, ask, bid_iv, ask_iv etc.
        """
        r = requests.get(
            f'{self.base_url}public/get_order_book?depth=5&instrument_name={instrument}')
        return r.json()['result']

    def get_latest_trade(self, instrument):
        """Get latest trade

        Arguments:
            instrument {str} -- 'BTC-22MAY20-9250-C'

        Returns:
            json -- Price, iv, instrument_name, index_price, direction, amount
        """
        r = requests.get(
            f'{self.base_url}public/get_last_trades_by_instrument?count=1&instrument_name={instrument}')
        return r.json()['result']
