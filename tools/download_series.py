#!/usr/bin/env python3

import sys
import yfinance as yf

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from datetime import date, datetime, timedelta
from backports.zoneinfo import ZoneInfo


def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    db = client.stockdata

    return db


def load_tickers(file):
    with open(file, 'r') as f:
        return f.readlines()


def read_info(db, s):
    res = db['info'].find_one({'symbol': s})

    return res


def download_dataset(symbol, start, end):
    d = yf.download(symbol, period='1d', interval='1m', start=start, end=end)

    return d


def query_forex(db, timestamp):
    print(timestamp)

    gmt = timestamp.replace(tzinfo=ZoneInfo('GMT'))

    res = db['forex'].find_one({'timestamp': gmt})
    print(res)
    return res


def insert_dataframes(db, d, s):
    a = read_info(db, s)

    for i in d.iterrows():
        if sys.argv[1] == 'data':
            if 'currency' in a and a['currency'] != 'EUR':
                forex = query_forex(db, i[0])

                if forex:
                    high_eur = forex['high'] * i[1][1]
                    low_eur = forex['low'] * i[1][2]
                    open_eur = forex['open'] * i[1][0]
                    close_eur = forex['close'] * i[1][3]
                    adjust_close_eur = forex['adjust_close'] * i[1][4]
            else:
                high_eur = i[1][1]
                low_eur = i[1][2]
                open_eur = i[1][0]
                close_eur = i[1][3]
                adjust_close_eur = i[1][4]

            data = {'timestamp': i[0], 'open': i[1][0], 'high': i[1][1],
                    'low': i[1][2], 'close': i[1][3], 'volume': i[1][5],
                    'adjust_close': i[1][4], 'high_eur': high_eur,
                    'close_eur': close_eur, 'open_eur': open_eur, 'symbol': s,
                    'low_eur': low_eur, 'adjust_close_eur': adjust_close_eur}
        else:
            data = {'timestamp': i[0], 'open': i[1][0], 'high': i[1][1],
                    'low': i[1][2], 'close': i[1][3], 'adjust_close': i[1][4],
                    'symbol': s}

        try:
            db[sys.argv[1]].insert_one(data)

            print(data)
        except DuplicateKeyError:
            print(f'ERROR: duplicate key {i[0]} with symbol {s}')


def handle_datestring(db, symbol, factor_start, factor_end):
    delta_end = timedelta(days=factor_end)
    initial_end_date = date.today().isoformat()
    end_iso_date = datetime.fromisoformat(initial_end_date) - delta_end

    delta_start = timedelta(days=factor_start)
    start_iso_date = datetime.fromisoformat(initial_end_date) - delta_start

    end_date = start_iso_date.strftime('%Y-%m-%d')
    start_date = end_iso_date.strftime('%Y-%m-%d')

    print(end_date, start_date)

    data = download_dataset(symbol, start_date, end_date)
    insert_dataframes(db, data, symbol)


def request_download(db, symbol, flag):
    if flag == 'full':
        for i in range(4):
            factor_end = i * 7 + 6

            if i > 0:
                factor_start = i * 7
            else:
                factor_start = i * 7 - 1

            handle_datestring(db, symbol, factor_start, factor_end)

        print()
    elif flag == 'short':
        factor_start = -1
        factor_end = 6

        handle_datestring(db, symbol, factor_start, factor_end)


db = connect_mongodb()

db[sys.argv[1]].create_index(
    [('symbol', ASCENDING), ('timestamp', ASCENDING)], unique=True
)

if len(sys.argv) == 4:
    # download_series.py data dax30.csv full
    t = load_tickers(sys.argv[2])
elif len(sys.argv) == 5:
    # download_series.py forex dax30.csv short USDEUR=X
    t = [sys.argv[4]]

for i in t:
    print(f'Going to download dataframes for {i.upper().strip()}')
    request_download(db, i.upper().strip(), sys.argv[3])
