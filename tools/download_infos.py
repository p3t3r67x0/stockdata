#!/usr/bin/env python3

import re
import sys
import yfinance as yf

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

from datetime import datetime


def connect_mongodb():
    c = MongoClient('mongodb://localhost:27017')

    return c['stockdata']


def load_tickers():
    with open(sys.argv[1], 'r') as f:
        return f.readlines()


def read_symbols(db):
    res = db['data'].distinct('symbol')

    return res


def read_symbol(db, symbol):
    res = db['info'].find_one({'symbol': symbol})

    return res


def update_information(db, symbol, info):
    now = datetime.utcnow()

    d = {}

    d['updated_at'] = now

    if 'fullTimeEmployees' in info:
        d['full_time_employees'] = info['fullTimeEmployees']

    if 'sector' in info:
        d['sector'] = info['sector']

    if 'zip' in info:
        d['zip'] = info['zip']

    if 'longBusinessSummary' in info:
        d['long_business_summary'] = info['longBusinessSummary']

    if 'city' in info:
        d['city'] = info['city']

    if 'phone' in info:
        d['phone'] = info['phone']

    if 'state' in info:
        d['state'] = info['state']

    if 'country' in info:
        d['country'] = info['country']

    if 'companyOfficers' in info:
        d['company_officers'] = info['companyOfficers']

    if 'website' in info:
        d['website'] = info['website']

    if 'maxAge' in info:
        d['max_age'] = info['maxAge']

    if 'address1' in info:
        d['address1'] = info['address1']

    if 'fax' in info:
        d['fax'] = info['fax']

    if 'industry' in info:
        d['industry'] = info['industry']

    if 'previousClose' in info:
        d['previous_close'] = info['previousClose']

    if 'regularMarketOpen' in info:
        d['regular_market_open'] = info['regularMarketOpen']

    if 'twoHundredDayAverage' in info:
        d['two_hundred_day_average'] = info['twoHundredDayAverage']

    if 'payoutRatio' in info:
        d['payout_ratio'] = info['payoutRatio']

    if 'volume24Hr' in info:
        d['volume_24_hours'] = info['volume24Hr']

    if 'regularMarketDayHigh' in info:
        d['regular_market_day_high'] = info['regularMarketDayHigh']

    if 'navPrice' in info:
        d['nav_price'] = info['navPrice']

    if 'averageDailyVolume10Day' in info:
        d['average_daily_volume_10_day'] = info['averageDailyVolume10Day']

    if 'totalAssets' in info:
        d['total_assets'] = info['totalAssets']

    if 'regularMarketPreviousClose' in info:
        d['regular_market_previous_close'] = info['regularMarketPreviousClose']

    if 'fiftyDayAverage' in info:
        d['fifty_day_average'] = info['fiftyDayAverage']

    if 'trailingAnnualDividendRate' in info:
        d['trailing_annual_dividend_rate'] = info['trailingAnnualDividendRate']

    if 'open' in info:
        d['open'] = info['open']

    if 'expireDate' in info:
        d['expire_date'] = info['expireDate']

    if 'algorithm' in info:
        d['algorithm'] = info['algorithm']

    if 'toCurrency' in info:
        d['to_currency'] = info['toCurrency']

    if 'averageVolume10days' in info:
        d['average_volume_10_days'] = info['averageVolume10days']

    if 'yield' in info:
        d['yield'] = info['yield']

    if 'dividendRate' in info:
        d['dividend_rate'] = info['dividendRate']

    if 'exDividendDate' in info:
        d['ex_dividend_date'] = info['exDividendDate']

    if 'beta' in info:
        d['beta'] = info['beta']

    if 'startDate' in info:
        d['start_date'] = info['startDate']

    if 'circulatingSupply' in info:
        d['circulating_supply'] = info['circulatingSupply']

    if 'regularMarketDayLow' in info:
        d['regular_market_day_low'] = info['regularMarketDayLow']

    if 'priceHint' in info:
        d['price_hint'] = info['priceHint']

    if 'currency' in info:
        d['currency'] = info['currency']

    if 'trailingPE' in info:
        d['trailing_pe'] = info['trailingPE']

    if 'regularMarketVolume' in info:
        d['regular_market_volume'] = info['regularMarketVolume']

    if 'lastMarket' in info:
        d['last_market'] = info['lastMarket']

    if 'maxSupply' in info:
        d['max_supply'] = info['maxSupply']

    if 'openInterest' in info:
        d['open_interest'] = info['openInterest']

    if 'marketCap' in info:
        d['market_cap'] = info['marketCap']

    if 'askSize' in info:
        d['ask_size'] = info['askSize']

    if 'volumeAllCurrencies' in info:
        d['volume_all_currencies'] = info['volumeAllCurrencies']

    if 'strikePrice' in info:
        d['strike_price'] = info['strikePrice']

    if 'bid' in info:
        d['bid'] = info['bid']

    if 'averageVolume' in info:
        d['average_volume'] = info['averageVolume']

    if 'dayLow' in info:
        d['day_low'] = info['dayLow']

    if 'ask' in info:
        d['ask'] = info['ask']

    if 'volume' in info:
        d['volume'] = info['volume']

    if 'ytdReturn' in info:
        d['ytd_return'] = info['ytdReturn']

    if 'fiftyTwoWeekHigh' in info:
        d['fifty_two_week_high'] = info['fiftyTwoWeekHigh']

    if 'forwardPE' in info:
        d['forward_pe'] = info['forwardPE']

    if 'tradeable' in info:
        d['tradeable'] = info['tradeable']

    if 'fromCurrency' in info:
        d['from_currency'] = info['fromCurrency']

    if 'fiveYearAvgDividendYield' in info:
        d['five_year_avg_dividend_yield'] = info['fiveYearAvgDividendYield']

    if 'fiftyTwoWeekLow' in info:
        d['fifty_two_week_low'] = info['fiftyTwoWeekLow']

    if 'dividendYield' in info:
        d['dividend_yield'] = info['dividendYield']

    if 'bidSize' in info:
        d['bid_size'] = info['bidSize']

    if 'dayHigh' in info:
        d['day_high'] = info['dayHigh']

    if 'exchange' in info:
        d['exchange'] = info['exchange']

    if 'shortName' in info:
        d['short_name'] = info['shortName']

    if 'exchangeTimezoneName' in info:
        d['exchange_timezone_name'] = info['exchangeTimezoneName']

    if 'isEsgPopulated' in info:
        d['is_esg_populated'] = info['isEsgPopulated']

    if 'gmtOffSetMilliseconds' in info:
        d['gmt_off_set_milliseconds'] = info['gmtOffSetMilliseconds']

    if 'quoteType' in info:
        d['quote_type'] = info['quoteType']

    if 'symbol' in info:
        d['symbol'] = info['symbol']

        if re.match(r'[\.]{1}', info['symbol']):
            d['symbol'] = info['symbol'].split('.')[0]

    if 'messageBoardId' in info:
        d['message_board_id'] = info['messageBoardId']

    if 'market' in info:
        d['market'] = info['market']

    if 'beta3Year' in info:
        d['beta_3_year'] = info['beta3Year']

    if 'annualHoldingsTurnover' in info:
        d['annual_holdings_turnover'] = info['annualHoldingsTurnover']

    if 'enterpriseToRevenue' in info:
        d['enterprise_to_revenue'] = info['enterpriseToRevenue']

    if 'profitMargins' in info:
        d['profit_margins'] = info['profitMargins']

    if 'enterpriseToEbitda' in info:
        d['enterprise_to_ebitda'] = info['enterpriseToEbitda']

    if '52WeekChange' in info:
        d['52_week_change'] = info['52WeekChange']

    if 'morningStarRiskRating' in info:
        d['morning_star_risk_rating'] = info['morningStarRiskRating']

    if 'longName' in info:
        d['long_name'] = info['longName']

    if 'forwardEps' in info:
        d['forward_eps'] = info['forwardEps']

    if 'revenueQuarterlyGrowth' in info:
        d['revenue_quarterly_growth'] = info['revenueQuarterlyGrowth']

    if 'sharesOutstanding' in info:
        d['shares_outstanding'] = info['sharesOutstanding']

    if 'fundInceptionDate' in info:
        d['fund_inception_date'] = info['fundInceptionDate']

    if 'annualReportExpenseRatio' in info:
        d['annual_report_expense_ratio'] = info['annualReportExpenseRatio']

    if 'bookValue' in info:
        d['book_value'] = info['bookValue']

    if 'sharesShort' in info:
        d['shares_short'] = info['sharesShort']

    if 'sharesPercentSharesOut' in info:
        d['shares_percent_shares_out'] = info['sharesPercentSharesOut']

    if 'fundFamily' in info:
        d['fund_family'] = info['fundFamily']

    if 'lastFiscalYearEnd' in info:
        d['last_fiscal_year_end'] = info['lastFiscalYearEnd']

    if 'heldPercentInstitutions' in info:
        d['held_percent_institutions'] = info['heldPercentInstitutions']

    if 'netIncomeToCommon' in info:
        d['net_income_to_common'] = info['netIncomeToCommon']

    if 'trailingEps' in info:
        d['trailing_eps'] = info['trailingEps']

    if 'lastDividendValue' in info:
        d['last_dividend_value'] = info['lastDividendValue']

    if 'SandP52WeekChange' in info:
        d['sand_p_52_week_change'] = info['SandP52WeekChange']

    if 'priceToBook' in info:
        d['price_to_book'] = info['priceToBook']

    if 'floatShares' in info:
        d['float_shares'] = info['floatShares']

    if 'heldPercentInsiders' in info:
        d['held_percent_insiders'] = info['heldPercentInsiders']

    if 'nextFiscalYearEnd' in info:
        d['next_fiscal_year_end'] = info['nextFiscalYearEnd']

    if 'mostRecentQuarter' in info:
        d['most_recent_quarter'] = info['mostRecentQuarter']

    if 'shortRatio' in info:
        d['short_ratio'] = info['shortRatio']

    if 'enterpriseValue' in info:
        d['enterprise_value'] = info['enterpriseValue']

    if 'threeYearAverageReturn' in info:
        d['three_year_average_return'] = info['threeYearAverageReturn']

    if 'lastSplitDate' in info:
        d['last_split_date'] = info['lastSplitDate']

    if 'lastSplitFactor' in info:
        d['last_split_factor'] = info['lastSplitFactor']

    if 'legalType' in info:
        d['legal_type'] = info['legalType']

    if 'lastCapGain' in info:
        d['last_cap_gain'] = info['lastCapGain']

    if 'lastDividendDate' in info:
        d['last_dividend_date'] = info['lastDividendDate']

    if 'morningStarOverallRating' in info:
        d['morning_star_overall_rating'] = info['morningStarOverallRating']

    if 'earningsQuarterlyGrowth' in info:
        d['earnings_quarterly_growth'] = info['earningsQuarterlyGrowth']

    if 'dateShortInterest' in info:
        d['date_short_interest'] = info['dateShortInterest']

    if 'pegRatio' in info:
        d['peg_ratio'] = info['pegRatio']

    if 'category' in info:
        d['category'] = info['category']

    if 'shortPercentOfFloat' in info:
        d['short_percent_of_float'] = info['shortPercentOfFloat']

    if 'sharesShortPriorMonth' in info:
        d['shares_short_prior_month'] = info['sharesShortPriorMonth']

    if 'impliedSharesOutstanding' in info:
        d['implied_shares_outstanding'] = info['impliedSharesOutstanding']

    if 'fiveYearAverageReturn' in info:
        d['five_year_average_return'] = info['fiveYearAverageReturn']

    if 'regularMarketPrice' in info:
        d['regular_market_price'] = info['regularMarketPrice']

    if 'logo_url' in info:
        d['logo_url'] = info['logo_url']

    db['info'].update_one({'symbol': symbol}, {'$set': d}, upsert=False)


def insert_essential(db, symbol, isin):
    try:
        db['info'].insert_one({'symbol': symbol, 'isin': isin})
    except DuplicateKeyError:
        print(f'ERROR: duplicate key with symbol {symbol}')


db = connect_mongodb()

db['info'].create_index(
    [('symbol', ASCENDING), ('isin', ASCENDING)], unique=True
)


for symbol in load_tickers():
    symbol = symbol.strip()
    res = read_symbol(db, symbol)

    if res is not None:
        continue

    info = yf.Ticker(symbol)
    print(f'Extracting info for {symbol} with ISIN {info.isin}')

    insert_essential(db, symbol, info.isin)
    update_information(db, symbol, info.info)
