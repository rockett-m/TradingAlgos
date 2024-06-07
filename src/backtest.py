#!/usr/bin/env python3
import os, sys
# scraping
import yfinance as yf
from bs4 import BeautifulSoup
# data manipulation
import pandas as pd
# data visualization
from collections import OrderedDict

from stock import stock_data

from backtesting import buy_and_hold_one_year
from backtesting import buy_at_open_sell_at_close
from backtesting import buy_at_close_sell_at_open
from backtesting import delta_high_low_yearly


from create_results import create_graph, create_csv


if __name__ == '__main__':
    # from https://www.nasdaq.com/market-activity/stocks/msft/historical?page=1&rows_per_page=10&timeline=y1)
    # order is latest data first and oldest data last

    # gather all the tickers from the data folder

    os.makedirs('results/backtesting', exist_ok=True)

    tickers = OrderedDict()
    for root, dirs, files in os.walk('data/nasdaq_1yr'):
        for file in files:
            filename = file.split('_')
            ticker = filename[0]
            if ticker not in tickers:
                tickers[ticker] = f'{root}/{file}'

    # dataframe to store the results with one ticker per row
    df_results = pd.DataFrame(columns=['ticker',
                                        'open_price ($)',
                                        'close_price ($)',
                                        'one_year ($)',
                                        'one_year (%)',
                                        'buy_open_sell_close ($)',
                                        'buy_open_sell_close (%)',
                                        'buy_close_sell_open ($)',
                                        'buy_close_sell_open (%)'])

    for idx, ticker in enumerate(tickers.keys()):
        # print(f'{ticker = }')

        stock = stock_data(ticker)

        stock.read_data()

        one_year, one_year_pct = buy_and_hold_one_year(stock)

        buy_open_sell_close, buy_open_sell_close_pct = buy_at_open_sell_at_close(stock)

        buy_close_sell_open, buy_close_sell_open_pct = buy_at_close_sell_at_open(stock)

        # unrealistic to buy at the low and sell at the high each day
        # not including in charts / results csv
        delta_high_low = delta_high_low_yearly(stock)

        # for results dataframe
        open_price, close_price = stock.open_price, stock.close_price

        one_year, one_year_pct = stock.yearly_return, stock.yearly_return_pct

        df_results.loc[idx] = [ticker,
                            open_price,
                            close_price,
                            one_year,
                            one_year_pct,
                            buy_open_sell_close,
                            buy_open_sell_close_pct,
                            buy_close_sell_open,
                            buy_close_sell_open_pct]

    # from create_results.py
    create_graph(df_results, save=True)
    create_csv(df_results, save=True)
