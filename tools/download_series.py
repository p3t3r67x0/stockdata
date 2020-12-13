#!/usr/bin/env python3

import yfinance as yf

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from datetime import date, datetime, timedelta


def connect_mongodb():
    c = MongoClient('mongodb://localhost:27017')

    return c['stockdata']


def load_tickers():
    with open('dax500.csv', 'r') as f:
        return f.readlines()


def download_dataset(symbol, start, end):
    d = yf.download(symbol, period='1d', interval='1m', start=start, end=end)

    return d


def insert_dataframes(d, s):
    a = yf.Ticker(s)

    for i in d.iterrows():
        try:
            c['data'].insert_one({'timestamp': i[0], 'open': i[1][0],
                                  'high': i[1][1], 'low': i[1][2],
                                  'close': i[1][3], 'volume': i[1][5],
                                  'adjust_close': i[1][4], 'symbol': s,
                                  'isin': a.isin})

            print(s, i[0], i[1][0], i[1][1], i[1]
                  [2], i[1][3], i[1][4], i[1][5])
        except DuplicateKeyError:
            print(f'ERROR: duplicate key {i[0]} with symbol {s}')


def request_download(symbol):
    for i in range(4):
        factor_start = i * 7 + 1
        factor_end = i * 7 + 7

        delta_end = timedelta(days=factor_end - 1)
        initial_end_date = date.today().isoformat()
        end_iso_date = datetime.fromisoformat(initial_end_date) - delta_end

        delta_start = timedelta(days=factor_start - 1)
        start_iso_date = datetime.fromisoformat(initial_end_date) - delta_start

        end_date = start_iso_date.strftime('%Y-%m-%d')
        start_date = end_iso_date.strftime('%Y-%m-%d')

        print(start_date, end_date)

        d = download_dataset(symbol, start_date, end_date)
        insert_dataframes(d, symbol)


c = connect_mongodb()

c['data'].create_index(
    [('symbol', ASCENDING), ('timestamp', ASCENDING)], unique=True
)

t = load_tickers()

for i in t:
    request_download(i.strip())
