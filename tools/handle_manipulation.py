#!/usr/bin/env python3

import re

from pymongo import MongoClient, DESCENDING
from bson import ObjectId


def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    db = client.stockdata

    return db


def read_dataframes(db):
    res = db['data'].find().sort([('timestamp', DESCENDING)]).limit(100000)

    return res


def remove_field(db, id, field):
    res = db['data'].update_one({'_id': ObjectId(id)}, {
                                '$unset': {field: True}})

    return res


db = connect_mongodb()


for i in range(1, 100):
    for frame in read_dataframes(db):
        print(f'processing {frame["_id"]} with {frame["symbol"]}')

        for item in frame:
            if re.match(r'.*_eur$', item):
                res = remove_field(db, frame['_id'], item)

                if res.modified_count > 0:
                    print(frame['_id'], item)
