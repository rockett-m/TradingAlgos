#!/usr/bin/env python3
import os, sys
# scraping
import yfinance as yf
from bs4 import BeautifulSoup
# data manipulation
import pandas as pd
import numpy as np
# data visualization
import matplotlib.pyplot as plt
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

    df_results = pd.DataFrame(columns=['ticker',
                                        'open_price ($)',
                                        'close_price ($)',
                                        'one_year ($)',
                                        'one_year (%)',
                                        'buy_open_sell_close ($)',
                                        'buy_open_sell_close (%)',
                                        'buy_close_sell_open ($)',
                                        'buy_close_sell_open (%)'])

    idx = 0
    for ticker, path in tickers.items():
        # print(f'{ticker = }')

        stock = stock_data(ticker)

        stock.read_data()

        one_year, one_year_pct = buy_and_hold_one_year(stock)

        buy_open_sell_close, buy_open_sell_close_pct = buy_at_open_sell_at_close(stock)

        buy_close_sell_open, buy_close_sell_open_pct = buy_at_close_sell_at_open(stock)

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
        idx += 1

    # show dataframe with results
    print(df_results)

    # plot the results
    fig, ax = plt.subplots()
    ax.plot(df_results['ticker'], df_results['one_year (%)'], label='Buy and Hold')
    ax.plot(df_results['ticker'], df_results['buy_open_sell_close (%)'], label='Buy at Open, Sell at Close')
    ax.plot(df_results['ticker'], df_results['buy_close_sell_open (%)'], label='Buy at Close, Sell at Open')
    ax.set_xlabel('Ticker')
    ax.set_ylabel('Return (%)')
    ax.set_title('Stock Returns')
    ax.legend()
    plt.show()

    # save graph to file
    fig.savefig('results/stock_returns.png')

    # save the results to a csv file
    df_results = df_results.round(2)
    df_results.to_csv('results/results.csv')
