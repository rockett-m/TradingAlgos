#!/usr/bin/env python3

import os, sys
import time
import tkinter
from tkinter import ttk
from matplotlib import pyplot as plt
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import selenium as sel
import pandas as pd
from io import StringIO
from datetime import datetime
import aiohttp
import asyncio
from collections import OrderedDict
import argparse
import math
import logging


metrics = ['gainers',
           'losers',
           'most-active',
           'trending-tickers']
        # failing at the moment \/
        #    'highest-implied-volatility',
        #    'highest-open-interest' ]

# status code, dataframe, runtime, filename
metrics_dict = OrderedDict((metric, [int, pd.DataFrame, 0.0, __file__]) for metric in metrics)

results_folder = 'results/yfinance'


def parse_args():
    parser = argparse.ArgumentParser(description='Scrape live stocks from Yahoo Finance')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug info')
    parser.add_argument('-v', '--visualize', action='store_true', help='Visualize the dataframes')
    return parser.parse_args()


# helper decorator to time functions
def timeit(method):
    async def wrapper(*args):
        metric = args[1]
        logging.debug(f'{method.__name__} for {metric} started...\n')

        start = time.time()
        result = await method(*args)
        finish = time.time()
        runtime = round(finish - start, 3)

        if metrics_dict[metric][0] != 200:
            logging.error(f'Error: {metric} data not found')
            return result

        metrics_dict[metric][2] = runtime
        return result
    return wrapper


# time this
@timeit
async def scrape_live_stocks(session, metric):
    # print(f'Attempting to scrape {metric} stocks...\n')

    website = f'https://finance.yahoo.com/{metric}/'

    async with session.get(website) as response:
        metrics_dict[metric][0] = response.status

        if response.status != 200: return

        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        # soup.prettify()

        # convert the data to a pandas dataframe
        df = pd.read_html(StringIO(str(soup)))[0]
        metrics_dict[metric][1] = df

        # convert to csv with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        filename = f'{results_folder}/{metric}_{timestamp}.csv'
        # overwrite of same tickers won't be an issue due to unique timestamps
        df.to_csv(filename, index=False)
        metrics_dict[metric][3] = filename


async def scrape_stocks():
    async with aiohttp.ClientSession() as session:
        operations = [scrape_live_stocks(session, metric) for metric in metrics]
        await asyncio.gather(*operations)


def create_table(frame, dataframe, style):
    table = ttk.Treeview(frame, show="headings", selectmode="browse")
    table["columns"] = list(dataframe.columns)
    for column in dataframe.columns:
        table.heading(column, text=column)
        table.column(column, width=100)

    # Apply tags for specific columns
    for i, row in enumerate(dataframe.itertuples(index=False)):
        tags = []
        if style == 'gainers' and row._4.startswith('+'):
            tags.append('gainers_change')
        if style == 'losers' and row._4.startswith('-'):
            tags.append('losers_change')
        if style == 'most_active':
            tags.append('most_active_volume')
        table.insert("", "end", values=row, tags=tags)

    # Tag configuration
    if style == 'gainers':
        table.tag_configure('gainers_change', foreground='green', font=('Helvetica', 10, 'bold'))
    elif style == 'losers':
        table.tag_configure('losers_change', foreground='red', font=('Helvetica', 10, 'bold'))
    elif style == 'most_active':
        table.tag_configure('most_active_volume', font=('Helvetica', 10, 'bold'))

    return table


if __name__ == '__main__':

    start_program = time.time()
    args = parse_args()
    # create log file in results dir with current timestamp
    log_filename = f'{results_folder}/scrape_live_stocks_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log'

    # Configure logging to file and console
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            # print to console \/
            # logging.StreamHandler()
        ]
    )
    logging.info(f'\nScraping live stock screeners from Yahoo Finance in parallel...\n')

    os.makedirs(results_folder, exist_ok=True)
    logging.debug(f'{results_folder = }\n')

    # parent function
    time_start = time.time()
    asyncio.run(scrape_stocks())
    time_end = time.time()
    total_time = round(time_end - time_start, 3)

    # previous_time = 0.0
    for metric, results in metrics_dict.items():
        runtime, filename = results[2], results[3]

        if results[0] != 200:
            logging.error(f'Error: {metric} data not found')
            continue

        logging.debug(f'metric: {metric.upper()} took {runtime} sec')
        logging.info(f'{filename = } generated\n')

    logging.debug(f'Time taken to scrape all metrics: {round(time_end - time_start, 3)} sec\n')

    # to print the dataframes and see the top rows of each metric
    num_rows = 5
    for metric, value in metrics_dict.items():
        df = value[1]
        # print the top 5 rows of each metric
        logging.info(f'{metric = }\n{df.head(num_rows)}\n')
        print(f'{metric = }\n{df.head(num_rows)}\n')

    end_program = time.time()
    logging.info(f'Minimum refresh rate: {math.ceil(end_program - start_program)} sec\n')

    logging.info(f'Log file: {log_filename}\n')
    print(f'Log file: {log_filename}\n')

    if args.visualize:
        # open the csv files in the default csv viewer for each metric and all ~30 rows
        # [os.system(f'open {value[3]}') for metric, value in metrics_dict.items() if value[0] == 200]

        root = tkinter.Tk()
        root.title("Top 5 Rows of Stock Screeners")

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        for title, df in zip(metrics_dict.keys(), [value[1] for value in metrics_dict.values()]):
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=title)
            style = 'default'
            if title == 'Gainers':
                style = 'gainers'
            elif title == 'Losers':
                style = 'losers'
            elif title == 'Most Active':
                style = 'most_active'
            table = create_table(frame, df.head(), style=style)
            table.pack(fill='both', expand=True)

        root.mainloop()
