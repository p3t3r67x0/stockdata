#!/usr/bin/env python3

import sys

from pymongo import MongoClient


def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    db = client.stockdata

    return db


def load_tickers(file):
    with open(file, 'r') as f:
        return f.readlines()


def update_marketindex(db, symbol, index):
    filter = {'symbol': symbol}
    update = {'$addToSet': {'market_index': index}}

    res = db['info'].update_one(filter, update)

    if res.modified_count > 0:
        print(f'INFO: added {symbol} to market {index}')


db = connect_mongodb()


if len(sys.argv) == 3:
    # update_market_index.py sandp500.csv sandp500
    t = load_tickers(sys.argv[1])

for i in t:
    symbol = i.upper().strip()
    print(f'Going to update market index for {symbol}')
    update_marketindex(db, symbol, sys.argv[2])
