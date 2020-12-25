#!/usr/bin/env python3

import math
import motor.motor_asyncio
import yfinance as yf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import ASCENDING, TEXT
from datetime import time, date, datetime, timedelta

from pydantic import BaseSettings
from pytz import timezone


class Settings(BaseSettings):
    app_name: str = 'stocklify'
    admin_email: str
    app_url: str

    class Config:
        env_file = '.env'


def is_nan(v):
    return math.isnan(v)


def percentage(current, previous):
    if current == previous:
        return 0.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0.0


def connect_mongodb():
    mongo_uri = 'mongodb://localhost:27017'
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    db = client.stockdata

    return db


def download_dataset(symbol, start, end):
    d = yf.download(symbol, period='1d', interval='1m', start=start, end=end)

    return d


def get_date_range():
    now = datetime.now()
    tsz = now.astimezone(timezone('Europe/London'))
    current = tsz.replace(tzinfo=None)
    midnight = datetime.combine(date.today(), datetime.min.time())
    opening = datetime.combine(date.today(), time(8, 30, 0))

    if current >= midnight and current <= opening:
        current = current - timedelta(days=1)

    weekday1 = current.weekday()

    if weekday1 == 5:
        current = current - timedelta(days=1)
    elif weekday1 == 6:
        current = current - timedelta(days=2)

    end = current - timedelta(days=1)

    start = datetime.combine(current.date(), datetime.max.time())
    end = datetime.combine(end.date(), datetime.max.time())

    return {'start': start.replace(microsecond=0),
            'end': end.replace(microsecond=0)}


async def read_average(db, symbol, field, days):
    data = {}

    dt = get_date_range()

    res = await db['data'].aggregate([
        {'$match': {'symbol': symbol, 'timestamp': {
            '$lt': dt['start'], '$gte': dt['end']}}},
        {'$group': {'_id': '$symbol', 'average':
                    {'$avg': f'${field}'}}},
        {'$limit': 1}]).to_list(length=1)

    if res and res[0]['average'] is not None and not is_nan(res[0]['average']):
        data['value'] = str(round(res[0]['average'], 2))
        data['start'] = dt['start'].strftime('%Y-%m-%d')
        data['end'] = dt['end'].strftime('%Y-%m-%d')

    return data


async def read_symbols(db):
    res = await db['info'].distinct('symbol')

    return res


async def read_market_short_info(db, index):
    res = await db['info'].aggregate([
        {'$match': {'market_index': {'$in': [index]}}},
        {'$sort': {'symbol': 1}},
        {'$project': {'_id': '$symbol', 'isin': '$isin',
                      'long_name': '$long_name'}}
    ]).to_list(length=10000)

    return res


async def read_short_info(db):
    res = await db['info'].aggregate([
        {'$sort': {'symbol': 1}},
        {'$project': {'_id': '$symbol', 'isin': '$isin',
                      'long_name': '$long_name'}}
    ]).to_list(length=10000)

    return res


async def read_info(db, symbol):
    res = await db['info'].find_one({'symbol': symbol})

    return res


async def lookup_query(db, q):
    res = await db['info'].aggregate([
        {'$match': {'$text': {'$search': q}}},
        {'$project': {'_id': 0, 'symbol': 1, 'isin': 1, 'long_name': 1}},
        {'$limit': 12}
    ]).to_list(length=10000)

    return res


async def read_volume_monthly_interval(db, symbol, start, end):
    res = await db['data'].aggregate([
        {'$match': {'symbol': symbol, 'timestamp': {
            '$lt': start, '$gte': end}}},
        {'$group': {'_id': {'$dayOfYear': '$timestamp'},
                    'high': {'$max': '$high_eur'},
                    'low': {'$min': '$low_eur'},
                    'open': {'$first': '$open_eur'},
                    'close': {'$last': '$close_eur'},
                    'volume': {'$sum': '$volume'}}},
        {'$sort': {'_id': 1}},
    ]).to_list(length=10000)

    return res


async def read_market_index(db, index, start, end):
    res = await db['info'].aggregate([
        {'$match': {'market_index': index}},
        {'$lookup': {'from': 'data', 'localField': 'symbol',
                     'foreignField': 'symbol', 'as': 'data'}},
        {'$unwind': '$data'},
        {'$project': {
            'symbol': '$symbol', 'long_name': '$long_name', 'data': '$data'}},
        {'$match': {'data.timestamp': {'$lte': start, '$gte': end}}},
        {'$group': {
            '_id': {'symbol': '$symbol',
                    'long_name': '$long_name',
                    'year': {'$year': '$data.timestamp'},
                    'mth': {'$month': '$data.timestamp'},
                    'dom': {
                        '$subtract': [
                            {'$dayOfMonth': '$data.timestamp'}, {
                                '$mod': [{
                                    '$dayOfMonth': '$data.timestamp'}, 1]}
                        ]}},
            'high': {'$max': '$data.high_eur'},
            'low': {'$min': '$data.low_eur'},
            'open': {'$first': '$data.open_eur'},
            'close': {'$last': '$data.close_eur'}}},
        {'$sort': {'year': 1, '_id.mth': 1, '_id.dom': 1}},
        {'$limit': 2000}
    ]).to_list(length=2000)

    if len(res) == 0:
        start = start - timedelta(days=1)
        end = start - timedelta(days=2)

        res = await read_market_index(db, index, start, end)

    return res


async def read_volume_daily_interval(db, symbol, start, end):
    add = 60 * 60000

    res = await db['data'].aggregate([
        {'$match': {'symbol': symbol, 'timestamp': {
            '$lt': start, '$gte': end}}},
        {'$group':
         {'_id': {'year': {'$year': {'$add': ['$timestamp', add]}},
                  'doy': {'$dayOfYear': {'$add': ['$timestamp', add]}},
                  'hrs': {'$hour': {'$add': ['$timestamp', add]}},
                  'min': {'$subtract': [{'$minute': {'$add': [
                      '$timestamp', add]}}, {'$mod': [
                          {'$minute': {'$add': ['$timestamp', add]}}, 15]}
                  ]}},
          'high': {'$max': '$high_eur'},
          'low': {'$min': '$low_eur'},
          'open': {'$first': '$open_eur'},
          'close': {'$last': '$close_eur'},
          'volume': {'$sum': '$volume'}
          }},
        {'$sort': {'year': 1, '_id.doy': 1, '_id.hrs': 1, '_id.min': 1}}
    ]).to_list(length=100)

    return res


async def read_volume_interval(db, symbol, interval):
    dates = []
    high = []
    low = []
    open = []
    close = []
    volumes = []

    dt = get_date_range()

    start = dt['start']
    end = dt['start'] - timedelta(days=int(interval))

    if int(interval) == 1:
        res = await read_volume_daily_interval(db, symbol, start, end)
    else:
        res = await read_volume_monthly_interval(db, symbol, start, end)

    for r in res:
        if int(interval) == 1:
            dt = r['_id']
            dtc = datetime.combine(date(r['_id']['year'], 1, 1), time(
                r['_id']['hrs'], r['_id']['min'], 0))
            dt = dtc + timedelta(days=r['_id']['doy'] - 1)
            hm = dt.strftime('%I:%M')
            dates.append(f'{hm}')
        else:
            dtc = datetime.combine(
                date(date.today().year, 1, 1), datetime.max.time())
            dt = dtc + timedelta(days=r['_id'] - 1)
            dates.append(f'{dt.day}.{dt.month}.')

        if r['high'] is not None:
            high.append(round(r['high'], 2))
        else:
            high.append(0)

        if r['low'] is not None:
            low.append(round(r['low'], 2))
        else:
            low.append(0)

        if r['open'] is not None:
            open.append(round(r['open'], 2))
        else:
            open.append(0)

        if r['close'] is not None:
            close.append(round(r['close'], 2))
        else:
            close.append(0)

        if r['volume'] is not None and not is_nan(r['volume']):
            volumes.append(int(r['volume']))
        else:
            volumes.append(0)

    return {'volumes': volumes, 'dates': dates, 'high': high,
            'low': low, 'open': open, 'close': close,
            'start': str(start.date()), 'end': str(end.date())}


async def read_percentage_differences(db, index):
    data = []

    dt = get_date_range()
    dt = get_date_range()

    start1 = dt['start']
    end1 = dt['end']

    start2 = start1 - timedelta(days=1)
    end2 = end1 - timedelta(days=1)

    res1 = await read_market_index(db, index, start1, end1)
    res2 = await read_market_index(db, index, start2, end2)

    if not res1 or not res2:
        return []

    for i in res1:
        dt = datetime(i['_id']['year'], i['_id']['mth'], i['_id']['dom'])
        d = str(dt.date())

        object = {'symbol': i['_id']['symbol']}
        object['long_name'] = i['_id']['long_name']
        object['data'] = []

        obj = {'date': d}

        obj['close'] = round(i['close'], 2)

        object['data'].append(obj)
        data.append(object)

    for i in res2:
        dt = datetime(i['_id']['year'], i['_id']['mth'], i['_id']['dom'])
        d = str(dt.date())

        for j in data:
            if 'symbol' in j and j['symbol'] == i['_id']['symbol']:
                obj = {'date': d}

                obj['close'] = round(i['close'], 2)

                j['data'].append(obj)

    for d in data:
        percent = percentage(d['data'][0]['close'], d['data'][1]['close'])

        if d['data'][0]['close'] < d['data'][1]['close']:
            d['percent'] = round(percent * - percent, 2)
        else:
            d['percent'] = round(percent, 2)

    data.sort(key=lambda x: x['percent'], reverse=True)

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


@app.get('/symbols/all')
async def list_all_symbols():
    values = await read_short_info(db)

    return {'values': [v for v in values]}


@app.get('/percentages/market/{index}')
async def list_market_percentages(index):
    values = await read_percentage_differences(db, index)

    return values


@app.get('/symbols/market/{index}')
async def list_market_symbols(index):
    values = await read_market_short_info(db, index)

    return {'values': [v for v in values]}


@app.get('/volume/{symbol}/{interval}')
async def volume_interval(symbol, interval):
    symbol = symbol.upper()

    res = await read_volume_interval(db, symbol, interval)

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
