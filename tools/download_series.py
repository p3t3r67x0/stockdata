#!/usr/bin/env python3

import sys
import yfinance as yf

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from datetime import date, datetime, timedelta
from pytz import timezone


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


def read_currency_value(db, symbol, timestamp):
    tsz = timestamp.astimezone(timezone('Europe/London'))
    ts = tsz.replace(tzinfo=None)
    start = ts - timedelta(hours=2)
    end = ts + timedelta(hours=2)

    res = db['forex'].aggregate([{
        '$match': {'symbol': symbol, 'timestamp': {
            '$gte': start, '$lte': end}}},
        {'$project': {'timestamp': 1, 'high': '$high', 'low': '$low',
                      'open': '$open', 'close': '$close',
                      'adjust_close': '$adjust_close',
                      'difference': {'$abs': [
                          {'$subtract': ["$timestamp", ts]}]}}},
        {'$sort': {'difference': 1}},
        {'$limit': 1}])

    res = list(res)[0]

    return res


def multiply_currencies(db, symbol, data):
    forex = read_currency_value(db, symbol, data[0])

    high = forex['high'] * data[1][1]
    low = forex['low'] * data[1][2]
    open = forex['open'] * data[1][0]
    close = forex['close'] * data[1][3]
    adjust_close = forex['adjust_close'] * data[1][4]

    return {'high': high, 'low': low, 'open': open,
            'close': close, 'adjust_close': adjust_close}


def insert_dataframes(db, d, s):
    a = read_info(db, s)

    usd = 'USDEUR=X'
    hkd = 'HKDEUR=X'
    inr = 'INREUR=X'

    for i in d.iterrows():
        if sys.argv[1] == 'data' and s not in [inr, hkd, usd]:
            if 'currency' in a and a['currency'] == 'USD':
                res = multiply_currencies(db, usd, i)

                high_eur = res['high']
                low_eur = res['low']
                open_eur = res['open']
                close_eur = res['close']
                adjust_close_eur = res['adjust_close']

            elif 'currency' in a and a['currency'] == 'HKD':
                res = multiply_currencies(db, hkd, i)

                high_eur = res['high']
                low_eur = res['low']
                open_eur = res['open']
                close_eur = res['close']
                adjust_close_eur = res['adjust_close']

            elif 'currency' in a and a['currency'] == 'INR':
                res = multiply_currencies(db, inr, i)

                high_eur = res['high']
                low_eur = res['low']
                open_eur = res['open']
                close_eur = res['close']
                adjust_close_eur = res['adjust_close']

            elif 'currency' in a and a['currency'] == 'EUR':
                high_eur = i[1][1]
                low_eur = i[1][2]
                open_eur = i[1][0]
                close_eur = i[1][3]
                adjust_close_eur = i[1][4]

            else:
                raise Exception

            data = {'timestamp': i[0], 'open': i[1][0], 'high': i[1][1],
                    'low': i[1][2], 'close': i[1][3], 'volume': i[1][5],
                    'adjust_close': i[1][4], 'high_eur': high_eur,
                    'close_eur': close_eur, 'open_eur': open_eur, 'symbol': s,
                    'low_eur': low_eur, 'adjust_close_eur': adjust_close_eur}

        elif sys.argv[1] == 'forex' and s in [inr, hkd, usd]:
            data = {'timestamp': i[0], 'open': i[1][0], 'high': i[1][1],
                    'low': i[1][2], 'close': i[1][3], 'adjust_close': i[1][4],
                    'symbol': s}

        else:
            raise Exception

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
        factor_end = 1

        handle_datestring(db, symbol, factor_start, factor_end)


db = connect_mongodb()

db[sys.argv[1]].create_index(
    [('symbol', ASCENDING), ('timestamp', ASCENDING)], unique=True
)

if len(sys.argv) == 4 and sys.argv[1] == 'data':
    # download_series.py data dax30.csv full
    t = load_tickers(sys.argv[2])
elif len(sys.argv) == 4 and sys.argv[1] == 'forex':
    # download_series.py forex USDEUR=X short
    t = [sys.argv[2]]

for i in t:
    print(f'Going to download dataframes for {i.upper().strip()}')
    request_download(db, i.upper().strip(), sys.argv[3])
