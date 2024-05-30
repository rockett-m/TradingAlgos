#!/usr/bin/env python3
import os, sys
# scraping
import requests
import yfinance as yf
from bs4 import BeautifulSoup
# data manipulation
import pandas as pd
import numpy as np
# data visualization
import matplotlib.pyplot as plt
import inspect
from collections import OrderedDict

from stock import stock_data

from backtesting import buy_and_hold_one_year
from backtesting import buy_at_open_sell_at_close
from backtesting import buy_at_close_sell_at_open


if __name__ == '__main__':

    # from https://www.nasdaq.com/market-activity/stocks/msft/historical?page=1&rows_per_page=10&timeline=y1)
    # order is latest data first and oldest data last

    # from stock.py

    tickers = OrderedDict()

    for root, dirs, files in os.walk('data/nasdaq_1yr'):
        for file in files:
            filename = file.split('_')
            ticker = filename[0]
            if ticker not in tickers:
                tickers[ticker] = f'{root}/{file}'

    for ticker, path in tickers.items():
        # print(f'{ticker = }')

        stock = stock_data(ticker)

        stock.read_data()

        stock.yearly_return = buy_and_hold_one_year(stock)

        buy_at_open_sell_at_close(stock)

        buy_at_close_sell_at_open(stock)

    # msft = stock_data('MSFT')

    # msft.read_data()

    # # backtesting.py : data/MSFT_1Y_Data.csv
    # msft.yearly_return = buy_and_hold_one_year(msft)

    # buy_at_open_sell_at_close(msft)
    # buy_at_close_sell_at_open(msft)


    # from algo.py
