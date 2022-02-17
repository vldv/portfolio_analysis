import numpy as np
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def tradedate_2_dtime(td):
    """ convert trade date as formatted by yfinance to a datetime object """
    td_str = str(int(td))
    y, m, d = int(td_str[:4]), int(td_str[4:6]), int(td_str[6:])
    return datetime(y, m, d)

def convert_to_usd(ticker_df, forex_df):
    """ convert history dataframe of a ticker with a forex history dataframe """
    common_index = ticker_df.index.intersection(forex_df.index)
    ticker_common = ticker_df.loc[common_index]
    forex_common = forex_df.loc[common_index]
    for col in ['Open', 'High', 'Low', 'Close', 'Dividends']:
        ticker_common[col] = ticker_common[col] * forex_common[col]
    return ticker_common


def ticker_2_priceevol(ticker_df, trade_date, forex_df=[]):
    """ for a given yf history and trade date (datetime), return the time/price date over the holding period.
    forex conversion is performed if a forex history is given """
    if len(forex_df)!=0:
        ticker_df = convert_to_usd(ticker_df, forex_df)
    ticker_df_ri = ticker_df.reset_index()
    date = ticker_df_ri['Date']
    price = ticker_df_ri['Close']
    since_trade = date - trade_date
    has_bought = since_trade > timedelta(0)
    T, P = date[has_bought], price[has_bought]
    return T, P


def ratio_to_reference(ticker_df, ref_df, trade_date):
    """ compute the ratio between a given ticker (history) and a reference ticker (history), at trade date """
    return ticker_df.loc[trade_date, 'Close'] / ref_df.loc[trade_date, 'Close']


def scale_data(ticker_df, ref_df, trade_date, forex):
    """ scale ticker (history) to ref ticker (history) so the time/price series of the tickers 'stems' from the ref plot """
    initial_ratio = ratio_to_reference(ticker_df, ref_df, trade_date)
    T, P = ticker_2_priceevol(ticker_df, trade_date, forex)
    return T, P/initial_ratio
