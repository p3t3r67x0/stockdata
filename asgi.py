#!/usr/bin/env python3

import math
import pytz
import motor.motor_asyncio
import yfinance as yf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import ASCENDING, TEXT
from datetime import date, datetime, timedelta

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'stocklify'
    admin_email: str
    app_url: str

    class Config:
        env_file = '.env'


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


async def read_average(db, symbol, field, days):
    data = {}
    naive_datetime = datetime.combine(date.today(), datetime.max.time())
    timezone = pytz.timezone('US/Eastern')
    now = timezone.localize(naive_datetime)
    weekday = now.weekday()

    if weekday == 5:
        now = now - timedelta(days=1)
    elif weekday == 6:
        now = now - timedelta(days=2)

    end = now - timedelta(days=days)

    res = await db['data'].aggregate([{'$match': {'symbol': symbol,
                                                  'timestamp': {'$lt': now,
                                                                '$gte': end}}},
                                      {'$group': {'_id': '$symbol', 'average':
                                                  {'$avg': f'${field}'}}},
                                      {'$limit': 1}]).to_list(length=1)

    if res and res[0]['average'] is not None and not is_nan(res[0]['average']):
        data['value'] = str(round(res[0]['average'], 2))
        data['start'] = now.strftime('%Y-%m-%d')
        data['end'] = end.strftime('%Y-%m-%d')

    return data


async def read_symbols(db):
    res = await db['info'].distinct('symbol')

    return res


async def read_short_info(db):
    res = await db['info'].aggregate([{'$sort': {'symbol': 1}},
                                      {'$project': {'_id': '$symbol',
                                                    'isin': '$isin',
                                                    'long_name': '$long_name'}}
                                      ]).to_list(length=100000)

    return res


async def read_info(db, symbol):
    res = await db['info'].find_one({'symbol': symbol})

    return res


async def lookup_query(db, q):
    res = await db['data'].aggregate([{'$match': {'$text': {'$search': q}}},
                                      {'$project': {'_id': 0, 'symbol': 1,
                                                    'isin': 1, 'long_name': 1}}
                                      ]).to_list(length=100000)

    return res


async def retrieve_info(db, symbol):
    res = await db['info'].find({'symbol': symbol}).to_list(length=10000)

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
    Settings().app_url
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
    results = await lookup_query(db, query)

    return {'results': [r for r in results]}


@app.get('/symbols')
async def list_all_symbols():
    symbols = await read_symbols(db)

    return {'symbols': [s for s in symbols]}


@app.get('/infos/short')
async def list_all_short_infos():
    values = await read_short_info(db)
    print(values)

    return {'values': [v for v in values]}


@app.get('/average/{symbol}')
async def average_values(symbol):
    object = {}

    symbol = symbol.upper()
    metadata = await read_info(db, symbol)
    symbols = await read_symbols(db)

    if symbol not in [s for s in symbols]:
        return {}

    high_two_days = await read_average(db, symbol, 'high_eur', 2)
    object['high_two_days'] = high_two_days

    high_ten_days = await read_average(db, symbol, 'high_eur', 10)
    object['high_ten_days'] = high_ten_days

    high_thirty_days = await read_average(db, symbol, 'high_eur', 30)
    object['high_thirty_days'] = high_thirty_days

    low_two_days = await read_average(db, symbol, 'low_eur', 2)
    object['low_two_days'] = low_two_days

    low_ten_days = await read_average(db, symbol, 'low_eur', 10)
    object['low_ten_days'] = low_ten_days

    low_thirty_days = await read_average(db, symbol, 'low_eur', 30)
    object['low_thirty_days'] = low_thirty_days

    open_two_days = await read_average(db, symbol, 'open_eur', 2)
    object['open_two_days'] = open_two_days

    open_ten_days = await read_average(db, symbol, 'open_eur', 10)
    object['open_ten_days'] = open_ten_days

    open_thirty_days = await read_average(db, symbol, 'open_eur', 30)
    object['open_thirty_days'] = open_thirty_days

    close_two_days = await read_average(db, symbol, 'close_eur', 2)
    object['close_two_days'] = close_two_days

    close_ten_days = await read_average(db, symbol, 'close_eur', 10)
    object['close_ten_days'] = close_ten_days

    close_thirty_days = await read_average(db, symbol, 'close_eur', 30)
    object['close_thirty_days'] = close_thirty_days

    adjust_two_days = await read_average(
        db, symbol, 'adjust_close_eur', 2)
    object['adjust_two_days'] = adjust_two_days

    adjust_ten_days = await read_average(
        db, symbol, 'adjust_close_eur', 10)
    object['adjust_ten_days'] = adjust_ten_days

    adjust_thirty_days = await read_average(
        db, symbol, 'adjust_close_eur', 30)
    object['adjust_thirty_days'] = adjust_thirty_days

    return {'averages': [object], 'symbol': symbol, 'isin': metadata['isin'],
            'long_name': metadata['long_name']}
