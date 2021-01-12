#!/usr/bin/env python3

import math
import holidays
import motor.motor_asyncio

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


async def substract_hours(dates):
    now = datetime.now()

    dtc_noh = datetime.combine(now.date(), time(9, 0, 0))
    dtc_ncl = datetime.combine(now.date(), time(17, 30, 0))

    for d in dates:
        if now <= dtc_noh and now >= dtc_ncl:
            d['start'] = d['start'] - timedelta(days=1)
            d['end'] = d['end'] - timedelta(days=1)

    return dates


async def previous_working_day(day):
    hol = holidays.HolidayBase()

    for i in range(date.today().year - 3, date.today().year + 3):
        hol.append({datetime(i, 1, 1): 'Neujahr'})
        hol.append({datetime(i, 4, 10): 'Karfreitag'})
        hol.append({datetime(i, 4, 13): 'Ostermontag'})
        hol.append({datetime(i, 5, 1): 'Tag der Arbeit'})
        hol.append({datetime(i, 5, 21): 'Christi Himmelfahrt'})
        hol.append({datetime(i, 6, 1): 'Pfingstmontag'})
        hol.append({datetime(i, 10, 3): 'Tag der dt. Einheit'})
        hol.append({datetime(i, 12, 24): 'Heiligabend'})
        hol.append({datetime(i, 12, 25): '1. Weihnachtsfeiertag'})
        hol.append({datetime(i, 12, 26): '2. Weihnachtsfeiertag'})
        hol.append({datetime(i, 12, 31): 'Silvester'})

    weekday = day.weekday()

    if weekday == 5:
        most_recent = day - timedelta(days=1)
    elif weekday == 6:
        most_recent = day - timedelta(days=2)
    else:
        most_recent = day

    if most_recent not in hol:
        return most_recent
    else:
        most_recent = most_recent - timedelta(days=1)
        return await previous_working_day(most_recent)


async def get_date_ranges(interval, period):
    dates = []

    now = datetime.now()
    tsz = now.astimezone(timezone('Europe/Berlin'))
    start = tsz.replace(tzinfo=None)
    dtc_start = datetime.combine(start.date(), datetime.min.time())
    dtc_end = datetime.combine(start.date(), datetime.max.time())

    if period > 1:
        dtc_end = dtc_end - timedelta(days=period)

    s = await previous_working_day(dtc_start)
    e = await previous_working_day(dtc_end)

    dates.append({'start': s, 'end': e})

    if interval > 0:
        for i in range(1, interval, period):
            dtd_start = dtc_start - timedelta(days=i)
            dtd_end = dtc_end - timedelta(days=i)

            dtc_start = datetime.combine(dtd_start.date(), datetime.min.time())
            dtc_end = datetime.combine(dtd_end.date(), datetime.max.time())

            s = await previous_working_day(dtc_start)
            e = await previous_working_day(dtc_end)

            dates.append({'start': s, 'end': e})

    return dates


async def read_average(db, symbol, field, period):
    data = {}

    dr = await get_date_ranges(interval=1, period=period)
    print(dr)

    res = await db['data'].aggregate([
        {'$match': {'symbol': symbol, 'timestamp':
                    {'$lte': dr[0]['end'], '$gte': dr[0]['start']}}},
        {'$group': {'_id': '$symbol', 'average': {'$avg': f'${field}'}}},
        {'$limit': 1}]).to_list(length=1)

    if res and res[0]['average'] is not None and not is_nan(res[0]['average']):
        data['value'] = str(round(res[0]['average'], 2))
        data['start'] = dr[0]['start'].date()
        data['end'] = dr[0]['end'].date()

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


async def read_monthly_volume(db, symbol, start, end):
    add = 60 * 60000

    res = await db['data'].aggregate([
        {'$match': {'symbol': symbol, 'timestamp':
                    {'$lt': start, '$gte': end}}},
        {'$group':
            {'_id': {'year': {'$year': {'$add': ['$timestamp', add]}},
                     'mth': {'$month': {'$add': ['$timestamp', add]}},
                     'dom': {'$dayOfMonth': {'$add': ['$timestamp', add]}}},
             'high': {'$max': '$high_eur'},
             'low': {'$min': '$low_eur'},
             'open': {'$first': '$open_eur'},
             'close': {'$last': '$close_eur'},
             'volume': {'$sum': '$volume'}}},
        {'$sort': {'_id.year': 1, '_id.mth': 1, '_id.dom': 1}},
        {'$limit': 100}
    ]).to_list(length=100)

    return res


async def read_newcommer_closes(db):
    res = await db['data'].aggregate([
        {'$match': {'close_eur': {'$lte': 4.60}}},
        {'$group':
            {'_id': '$symbol', 'close_eur': {'$last': '$close_eur'},
             'timestamp': {'$max': '$timestamp'}}},
        {'$lookup': {'from': 'info', 'localField': '_id',
                     'foreignField': 'symbol', 'as': 'info'}},
        {'$unwind': '$info'},
        {'$project':
            {'industry': '$info.industry', 'timestamp': '$timestamp',
             'long_name': '$info.long_name', 'close_eur': '$close_eur'}},
        {'$sort': {'close_eur': {'$meta': 'textScore'}}},
        {'$limit': 250}
    ]).to_list(length=250)

    return res


async def read_market_index(db, index, start, end):
    res = await db['info'].aggregate([
        {'$match': {'market_index': index}},
        {'$lookup': {'from': 'data', 'localField': 'symbol',
                     'foreignField': 'symbol', 'as': 'data'}},
        {'$unwind': '$data'},
        {'$project':
            {'symbol': '$symbol', 'long_name': '$long_name', 'data': '$data'}},
        {'$match': {'data.timestamp': {'$lte': end, '$gte': start}}},
        {'$group':
            {'_id':
                {'symbol': '$symbol', 'long_name': '$long_name',
                 'year': {'$year': '$data.timestamp'},
                 'mth': {'$month': '$data.timestamp'},
                 'dom':
                     {'$subtract': [
                         {'$dayOfMonth': '$data.timestamp'},
                         {'$mod': [{'$dayOfMonth': '$data.timestamp'}, 1]}]}},
             'high': {'$max': '$data.high_eur'},
             'low': {'$min': '$data.low_eur'},
             'open': {'$first': '$data.open_eur'},
             'close': {'$last': '$data.close_eur'}}},
        {'$sort': {'_id.year': 1, '_id.mth': 1, '_id.dom': 1}},
        {'$limit': 25000}
    ]).to_list(length=25000)

    return res


async def read_daily_volume(db, symbol, start, end):
    add = 60 * 60000

    res = await db['data'].aggregate([
        {'$match':
            {'symbol': symbol, 'timestamp': {'$lte': end, '$gte': start}}},
        {'$group':
            {'_id': {'year': {'$year': {'$add': ['$timestamp', add]}},
                     'mth': {'$month': {'$add': ['$timestamp', add]}},
                     'dom': {'$dayOfMonth': {'$add': ['$timestamp', add]}},
                     'hrs': {'$hour': {'$add': ['$timestamp', add]}},
                     'min': {'$minute': {'$add': ['$timestamp', add]}}},
             'high': {'$max': '$high_eur'},
             'low': {'$min': '$low_eur'},
             'open': {'$first': '$open_eur'},
             'close': {'$last': '$close_eur'},
             'volume': {'$sum': '$volume'}}},
        {'$sort':
            {'year': 1, '_id.mth': 1, '_id.dom': 1,
             '_id.hrs': 1, '_id.min': 1}}
    ]).to_list(length=250)

    return res


async def read_volume_period(db, symbol, period):
    values = []

    dr = await get_date_ranges(interval=1, period=period)

    start = dr[0]['start']
    end = dr[0]['end']

    if period == 1:
        res = await read_daily_volume(db, symbol, start, end)
    else:
        res = await read_monthly_volume(db, symbol, start, end)

    for r in res:
        array = []

        if period == 1:
            dtc = datetime.combine(date(
                r['_id']['year'], r['_id']['mth'], r['_id']['dom']),
                time(r['_id']['hrs'], r['_id']['min'], 0))
            array.append(int(dtc.timestamp() * 1000))
        else:
            tm = datetime.min.time()
            dtc = datetime.combine(date(
                r['_id']['year'], r['_id']['mth'], r['_id']['dom']), tm)
            array.append(int(dtc.timestamp() * 1000))

        if r['open'] is not None:
            array.append(round(r['open'], 2))
        else:
            array.append(0.0)

        if r['high'] is not None:
            array.append(round(r['high'], 2))
        else:
            array.append(0.0)

        if r['low'] is not None:
            array.append(round(r['low'], 2))
        else:
            array.append(0.0)

        if r['close'] is not None:
            array.append(round(r['close'], 2))
        else:
            array.append(0.0)

        if r['volume'] is not None and not is_nan(r['volume']):
            array.append(int(r['volume']))
        else:
            array.append(0)

        values.append(array)

    return {'values': values, 'start': str(start.date()),
            'end': str(end.date())}


async def read_percentages(db, index):
    data = []

    dr = await get_date_ranges(interval=2, period=1)

    res1 = await read_market_index(db, index, dr[0]['start'], dr[0]['end'])
    res2 = await read_market_index(db, index, dr[1]['start'], dr[1]['end'])

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
        try:
            percent = percentage(d['data'][0]['close'], d['data'][1]['close'])

            if d['data'][0]['close'] < d['data'][1]['close']:
                d['percent'] = round(percent * - percent, 2)
            else:
                d['percent'] = round(percent, 2)
        except IndexError:
            del d

    try:
        data.sort(key=lambda x: x['percent'], reverse=True)
    except KeyError:
        pass

    return data


async def retrieve_info(db, symbol):
    res = await db['info'].find({'symbol': symbol}).to_list(length=100000)

    return res


app = FastAPI()
db = connect_mongodb()

db['data'].create_index(
    [('symbol', ASCENDING),
     ('timestamp', ASCENDING)], unique=True
)

db['info'].create_index(
    [('long_name', TEXT),
     ('industry', TEXT),
     ('symbol', TEXT),
     ('isin', TEXT)], name='query_index'
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


@app.get('/newcommers/all')
async def list_all_newcommers():
    values = await read_newcommer_closes(db)
    data = []

    for v in values:
        if 'close_eur' in v:
            v['close_eur'] = format(round(v['close_eur'], 2), '.2f')
        if 'timestamp' in v:
            v['timestamp'] = v['timestamp'].date()
        if 'industry' in v:
            v['industry'] = v['industry'].replace('—', '-')

        data.append(v)

    return {'values': data}


@app.get('/percentages/market/{index}')
async def list_market_percentages(index):
    values = await read_percentages(db, index)

    return values


@app.get('/symbols/market/{index}')
async def list_market_symbols(index):
    values = await read_market_short_info(db, index)

    return {'values': [v for v in values]}


@app.get('/volume/{symbol}/{period:int}')
async def list_volumes(symbol, period):
    symbol = symbol.upper()

    res = await read_volume_period(db, symbol, period)

    return res


@app.get('/average/{symbol}')
async def average_values(symbol):
    object = {}

    symbol = symbol.upper()
    meta = await read_info(db, symbol)
    symbols = await read_symbols(db)

    if symbol not in [s for s in symbols]:
        return object

    high_intra_day = await read_average(db, symbol, 'high_eur', 1)
    print(high_intra_day)
    object['high_intra_day'] = high_intra_day

    high_ten_days = await read_average(db, symbol, 'high_eur', 10)
    object['high_ten_days'] = high_ten_days

    high_thirty_days = await read_average(db, symbol, 'high_eur', 30)
    object['high_thirty_days'] = high_thirty_days

    low_intra_day = await read_average(db, symbol, 'low_eur', 1)
    object['low_intra_day'] = low_intra_day

    low_ten_days = await read_average(db, symbol, 'low_eur', 10)
    object['low_ten_days'] = low_ten_days

    low_thirty_days = await read_average(db, symbol, 'low_eur', 30)
    object['low_thirty_days'] = low_thirty_days

    open_intra_day = await read_average(db, symbol, 'open_eur', 1)
    object['open_intra_day'] = open_intra_day

    open_ten_days = await read_average(db, symbol, 'open_eur', 10)
    object['open_ten_days'] = open_ten_days

    open_thirty_days = await read_average(db, symbol, 'open_eur', 30)
    object['open_thirty_days'] = open_thirty_days

    close_intra_day = await read_average(db, symbol, 'close_eur', 1)
    object['close_intra_day'] = close_intra_day

    close_ten_days = await read_average(db, symbol, 'close_eur', 10)
    object['close_ten_days'] = close_ten_days

    close_thirty_days = await read_average(db, symbol, 'close_eur', 30)
    object['close_thirty_days'] = close_thirty_days

    adjust_intra_day = await read_average(
        db, symbol, 'adjust_close_eur', 1)
    object['adjust_intra_day'] = adjust_intra_day

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
