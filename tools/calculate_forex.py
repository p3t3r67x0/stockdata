#!/usr/bin/env python3

from pymongo import MongoClient, ASCENDING
from bson import ObjectId


def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    db = client.stockdata

    return db


def read_dataframes(db):
    res = db['data'].find().sort([('timestamp', ASCENDING)]).limit(100000)

    return res


def update_field(db, id, field, value):
    data = {f'{field}_eur': value}

    res = db['data'].update_one({'_id': ObjectId(id)}, {'$set': data})

    return res


def forex_usd_eur(db, id, field):
    res = db['data'].aggregate([{'$match': {'_id': ObjectId(id)}},
                                {'$lookup': {'from': 'forex',
                                             'localField': 'timestamp',
                                             'foreignField': 'timestamp',
                                             'as': 'forex'}},
                                {'$unwind': '$forex'},
                                {'$project': {'_id': '$_id',
                                              'timestamp': '$timestamp',
                                              f'{field}': {'$multiply':
                                                           [f'${field}',
                                                            f'$forex.{field}']}
                                              }},
                                {'$limit': 1}])

    return res


db = connect_mongodb()

fields = ['high', 'low', 'open', 'close', 'adjust_close']

for frame in read_dataframes(db):
    for field in fields:
        res = list(forex_usd_eur(db, frame['_id'], field))

        if len(res) > 0:
            r = update_field(db, res[0]['_id'], field, res[0][field])

            if r.modified_count > 0:
                print(frame['symbol'], res[0]['_id'],
                      res[0]['timestamp'], res[0][field])
