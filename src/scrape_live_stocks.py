#!/usr/bin/env python3

import os, sys
import time
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import selenium as sel
import pandas as pd
from io import StringIO
from datetime import datetime

# helper decorator to time functions
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f'\n{method.__name__} took: {round(te - ts, 3)} sec')
        return result
    return timed


metrics = ['most-active',
           'gainers',
           'losers',
           'trending-tickers' ]
        # failing at the moment \/
        #    'highest-implied-volatility',
        #    'highest-open-interest' ]

# time this
@timeit
def scrape_live_stocks(metric='most-active', debug=True):
    print(f'Attempting to scrape {metric} stocks...\n')

    results_folder = 'results/yfinance'
    os.makedirs(results_folder, exist_ok=True)

    website = f'https://finance.yahoo.com/{metric}/'

    response = requests.get(website)
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        print(f'Failed to scrape {metric} stocks!')
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    # soup.prettify()

    # convert the data to a pandas dataframe
    df = pd.read_html(StringIO(str(soup)))[0]
    if debug: print(df)

    # convert to csv with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{results_folder}/{metric}_{timestamp}.csv'
    # overwrite won't be an issue due to unique timestamps
    df.to_csv(filename, index=False)

    print(f'\n{filename = } generated')
    print(f'\n{metric} stocks scraped successfully!')


for idx, metric in enumerate(metrics):
    print(f'\n{metric = }')

    # if idx < 3:
    scrape_live_stocks(metric, debug=True)
