"""
This module contains functions to create a graph and a CSV file with the results of the backtesting.
"""

import os

PATH_STOCKS = 'data/kaggle/stocks/'
PATH_ETFS = 'data/kaggle/etfs/'

# scraping
for (root, dirs, files) in os.walk(PATH_STOCKS):
    for file in files:
        if file.endswith('.csv'):
            print(file)

            ticker = file.split('.')[0]
            print(ticker)
