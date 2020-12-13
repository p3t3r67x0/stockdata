#!/usr/bin/env python3

import math
import motor.motor_asyncio
import yfinance as yf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import ASCENDING, TEXT
from pymongo.errors import DuplicateKeyError

from datetime import date, datetime, timedelta


def is_nan(v):
    return math.isnan(v)


def connect_mongodb():
    mongo_uri = 'mongodb://localhost:27017'
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    db = client.stockdata

    return db


def download_dataset(symbol, start, end):
    d = yf.download(symbol, period='1d', interval='1m', start=start, end=end)

    return d


async def insert_dataframes(db, d, s):
    a = yf.Ticker(s)

    for i in d.iterrows():
        try:
            await db['data'].insert_one({'timestamp': i[0], 'open': i[1][0],
                                         'high': i[1][1], 'low': i[1][2],
                                         'close': i[1][3], 'volume': i[1][5],
                                         'adjust_close': i[1][4], 'symbol': s,
                                         'isin': a.isin})

            print(s, i[0], i[1][0], i[1][1], i[1]
                  [2], i[1][3], i[1][4], i[1][5])
        except DuplicateKeyError:
            print(f'ERROR: duplicate key {i[0]} with symbol {s}')


async def request_download(symbol):
    factor_start = 0
    factor_end = 7

    delta_end = timedelta(days=factor_end)
    initial_end_date = date.today().isoformat()
    end_iso_date = datetime.fromisoformat(initial_end_date) - delta_end

    delta_start = timedelta(days=factor_start)
    start_iso_date = datetime.fromisoformat(initial_end_date) - delta_start

    end_date = start_iso_date.strftime('%Y-%m-%d')
    start_date = end_iso_date.strftime('%Y-%m-%d')

    print(start_date, end_date)

    data = download_dataset(symbol, start_date, end_date)
    await insert_dataframes(data, symbol)


async def read_average(col, symbol, field, days):
    data = {}
    now = datetime.today()
    weekday_now = now.weekday()

    if weekday_now == 5:
        now = now - timedelta(days=1)
    elif weekday_now == 6:
        now = now - timedelta(days=2)

    end = now - timedelta(days=days)

    res = await col.aggregate([{'$match': {'symbol': symbol, 'timestamp':
                                           {'$lt': now, '$gte': end}}},
                               {'$group': {'_id': '$symbol', 'average':
                                           {'$avg': f'${field}'}}},
                               {'$limit': 1}]).to_list(length=1)

    if res and res[0]['average'] is not None and not is_nan(res[0]['average']):
        data['value'] = str(round(res[0]['average'], 2))
        data['start'] = now.strftime('%Y-%m-%d')
        data['end'] = end.strftime('%Y-%m-%d')

    return data


async def read_symbols(col):
    res = await col.distinct('symbol')

    return res


async def lookup_query(col, q):
    res = await col.aggregate([{'$match': {'$text': {'$search': q}}},
                               {'$project': {'_id': 0, 'symbol': 1, 'isin': 1,
                                             'long_name': 1, 'score':
                                                 {'$meta': 'textScore'}}}
                               ]).to_list(length=10000)

    return res


app = FastAPI()
db = connect_mongodb()

db['data'].create_index(
    [('symbol', ASCENDING), ('timestamp', ASCENDING)], unique=True
)

db['info'].create_index(
    [('long_name', TEXT), ('symbol', TEXT), ('isin', TEXT)], name='query_index'
)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/query/{query}')
async def list_results(query):
    results = await lookup_query(db['info'], query)

    return {'results': [r for r in results]}


@app.get('/symbols')
async def list_all_symbols():
    symbols = await read_symbols(db['info'])

    return {'symbols': [s for s in symbols]}


@app.get('/average/{symbol}')
async def average_values(symbol):
    object = {}

    symbol = symbol.upper()
    symbols = await read_symbols(db['info'])

    if symbol not in [s for s in symbols]:
        return {}, 404

    # fetch latest indicies
    # await request_download(symbol)

    high_one_day = await read_average(db['data'], symbol, 'high', 1)
    object['high_one_day'] = high_one_day

    high_ten_days = await read_average(db['data'], symbol, 'high', 10)
    object['high_ten_days'] = high_ten_days

    high_thirty_days = await read_average(db['data'], symbol, 'high', 30)
    object['high_thirty_days'] = high_thirty_days

    low_one_day = await read_average(db['data'], symbol, 'low', 1)
    object['low_one_day'] = low_one_day

    low_ten_days = await read_average(db['data'], symbol, 'low', 10)
    object['low_ten_days'] = low_ten_days

    low_thirty_days = await read_average(db['data'], symbol, 'low', 30)
    object['low_thirty_days'] = low_thirty_days

    open_one_day = await read_average(db['data'], symbol, 'open', 1)
    object['open_one_day'] = open_one_day

    open_ten_days = await read_average(db['data'], symbol, 'open', 10)
    object['open_ten_days'] = open_ten_days

    open_thirty_days = await read_average(db['data'], symbol, 'open', 30)
    object['open_thirty_days'] = open_thirty_days

    close_one_day = await read_average(db['data'], symbol, 'close', 1)
    object['close_one_day'] = close_one_day

    close_ten_days = await read_average(db['data'], symbol, 'close', 10)
    object['close_ten_days'] = close_ten_days

    close_thirty_days = await read_average(db['data'], symbol, 'close', 30)
    object['close_thirty_days'] = close_thirty_days

    adjust_one_day = await read_average(db['data'], symbol, 'adjust_close', 1)
    object['adjust_one_day'] = adjust_one_day

    adjust_ten_days = await read_average(
        db['data'], symbol, 'adjust_close', 10)
    object['adjust_ten_days'] = adjust_ten_days

    adjust_thirty_days = await read_average(
        db['data'], symbol, 'adjust_close', 30)
    object['adjust_thirty_days'] = adjust_thirty_days

    return {'averages': [object]}
