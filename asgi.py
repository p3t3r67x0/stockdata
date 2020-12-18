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
    dt = datetime.combine(date.today(), datetime.max.time())
    tz_name = dt.astimezone().tzname()
    tz = pytz.timezone(tz_name)
    now = tz.localize(dt)
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
    res = await db['info'].aggregate([{'$match': {'$text': {'$search': q}}},
                                      {'$project': {'_id': 0, 'symbol': 1,
                                                    'isin': 1, 'long_name': 1}
                                       }, {'$limit': 12}
                                      ]).to_list(length=100000)

    return res


async def read_volume_interval(db, symbol):
    data = []

    dt = datetime.combine(date.today(), datetime.max.time())
    tz_name = dt.astimezone().tzname()
    tz = pytz.timezone(tz_name)
    now = tz.localize(dt)
    weekday = now.weekday()

    if weekday == 5:
        now = now - timedelta(days=1)
    elif weekday == 6:
        now = now - timedelta(days=2)

    end = now - timedelta(days=30)

    res = await db['data'].aggregate([{'$match': {'symbol': symbol,
                                                  'timestamp': {'$lt': now,
                                                                '$gte': end}}},
                                      {'$group': {'_id':
                                                  {'$dayOfYear': '$timestamp'},
                                                  'high': {
                                                      '$last': '$high_eur'},
                                                  'low': {
                                                      '$last': '$low_eur'},
                                                  'open': {
                                                      '$last': '$open_eur'},
                                                  'close': {
                                                      '$last': '$close_eur'},
                                                  'volume': {'$sum': '$volume'}
                                                  }},
                                      {'$sort': {'_id': -1}},
                                      ]).to_list(length=100000)

    for r in res:
        dt = datetime.combine(
            date(date.today().year, 1, 1), datetime.max.time())
        d = dt + timedelta(days=r['_id'] - 1)
        ts = datetime.timestamp(d.replace(microsecond=0)) * 1000

        data.append([ts, round(r['open'], 2),
                     round(r['high'], 2), round(r['low'], 2),
                     round(r['close'], 2), round(r['volume'], 2)])

    return data


async def retrieve_info(db, symbol):
    res = await db['info'].find({'symbol': symbol}).to_list(length=100000)

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


@app.get('/infos/short')
async def list_all_short_infos():
    values = await read_short_info(db)

    return {'values': [v for v in values]}


@app.get('/volume/{symbol}')
async def volume_interval(symbol):
    symbol = symbol.upper()

    res = await read_volume_interval(db, symbol)

    return res


@app.get('/average/{symbol}')
async def average_values(symbol):
    object = {}

    symbol = symbol.upper()
    meta = await read_info(db, symbol)
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

    isin = ''
    long_name = ''
    zip = ''
    industry = ''
    address = ''
    long_business_summary = ''
    city = ''
    website = ''
    country = ''

    if 'isin' in meta:
        isin = meta['isin']

    if 'long_name' in meta:
        long_name = meta['long_name']

    if 'zip' in meta:
        zip = meta['zip']

    if 'industry' in meta:
        industry = meta['industry']

    if 'address1' in meta:
        address = meta['address1']

    if 'long_business_summary' in meta:
        long_business_summary = meta['long_business_summary']

    if 'city' in meta:
        city = meta['city']

    if 'website' in meta:
        website = meta['website']

    if 'country' in meta:
        country = meta['country']

    return {'averages': object, 'symbol': symbol, 'country': country,
            'long_name': long_name, 'zip': zip, 'industry': industry,
            'address': address, 'city': city, 'website': website,
            'isin': isin, 'long_business_summary': long_business_summary}
