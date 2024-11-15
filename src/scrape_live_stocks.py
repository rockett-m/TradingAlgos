#!/usr/bin/env python3
"""
This module contains functions to scrape live stocks from Yahoo Finance.
It uses the aiohttp library to make asynchronous requests to the Yahoo Finance website.
After the parallel requests are completed, the data is saved to CSV files and displayed in a tkinter window.
(trading_env) python3 -m src.scrape_live_stocks
"""

import os, sys
import time
from datetime import datetime
import argparse
from collections import OrderedDict
import math
import logging
from io import StringIO
import asyncio
import tkinter
from tkinter import ttk
import pandas as pd
import aiohttp
from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.dirname(os.path.join(__file__, "../../")))
sys.path.append(ROOT)

from utils.utils import path_check
# future imports potentially
# import yfinance as yf
# import requests
# import selenium as sel

RESULTS_FOLDER = os.path.join(ROOT, "results/yfinance")
os.makedirs(RESULTS_FOLDER, exist_ok=True)
for directory in [ROOT, RESULTS_FOLDER]:
    path_check(directory)


METRICS = ['gainers',
           'losers',
           'most-active',
           'trending-tickers']
        # failing at the moment \/
        #    'highest-implied-volatility',
        #    'highest-open-interest' ]

# status code, dataframe, runtime, filename
metrics_dict = OrderedDict((metric, [int, pd.DataFrame, 0.0, __file__]) for metric in METRICS)


def parse_args():
    parser = argparse.ArgumentParser(description='Scrape live stocks from Yahoo Finance')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug info')
    parser.add_argument('-v', '--visualize', action='store_true', help='Visualize the dataframes')
    return parser.parse_args()


def timeit(method):
    """
    A decorator that measures the runtime of an asynchronous method and logs the result.

    Args:
        method: The asynchronous method to be decorated.

    Returns:
        The decorated method.

    Example usage:
        @timeit
        async def my_async_method():
            # code goes here
    """
    async def wrapper(*args):
        category = args[1]
        logging.debug("%s for %s started...\n", method.__name__, category)

        start = time.time()
        result = await method(*args)
        finish = time.time()
        runtime = round(finish - start, 3)

        if metrics_dict[category][0] != 200:
            logging.error("Error: %s data not found", category)
            return result

        metrics_dict[category][2] = runtime
        return result
    return wrapper


@timeit
async def scrape_live_stocks(session, metric: str):
    """
    Scrapes live stocks data from Yahoo Finance for a given metric.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        metric (str): The metric for which to scrape stocks data.

    Returns:
        None: If the response status is not 200.
        pandas.DataFrame: The scraped stocks data as a pandas DataFrame.

    Raises:
        None.
    """
    # print(f'Attempting to scrape {metric} stocks...\n')

    website = f"https://finance.yahoo.com/{metric}/"

    async with session.get(website) as response:
        metrics_dict[metric][0] = response.status

        if response.status != 200:
            print(f"\nIs live streaming available now?\n\thttp get {response.status = }")
            return

        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        # soup.prettify()

        # convert the data to a pandas dataframe
        dataf = pd.read_html(StringIO(str(soup)))[0]
        metrics_dict[metric][1] = dataf

        # convert to csv with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        file_name = os.path.join(RESULTS_FOLDER, f"{metric}_{timestamp}.csv")
        # overwrite of same tickers won't be an issue due to unique timestamps
        dataf.to_csv(file_name, index=False)
        metrics_dict[metric][3] = file_name


async def scrape_stocks():
    async with aiohttp.ClientSession() as session:
        operations = [scrape_live_stocks(session, metric) for metric in METRICS]
        await asyncio.gather(*operations)


def create_table(frame, dataframe, style):
    """
    Create a table with the given dataframe and style.

    Args:
        frame (tkinter.Frame): The frame to place the table in.
        dataframe (pd.DataFrame): The dataframe to display.
        style (str): The style of the table.

    Returns:
        ttk.Treeview: The table widget.
    """
    table = ttk.Treeview(frame, show="headings", selectmode="browse")
    table["columns"] = list(dataframe.columns)
    for column in dataframe.columns:
        table.heading(column, text=column)
        table.column(column, width=100)

    # Apply tags for specific columns
    for _, row in enumerate(dataframe.itertuples(index=False)):
        tags = []
        if style == 'gainers' and row.startswith('+'):
            tags.append('gainers_change')
        if style == 'losers' and row.startswith('-'):
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
    log_filename = f"""{RESULTS_FOLDER}/scrape_live_stocks_{datetime.now()
                        .strftime("%Y-%m-%d_%H:%M:%S")}.log"""

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
    logging.info("\nScraping live stock screeners from Yahoo Finance in parallel...\n")
    logging.debug("RESULTS_FOLDER = %s\n", RESULTS_FOLDER)

    # parent function
    time_start = time.time()
    asyncio.run(scrape_stocks())
    time_end = time.time()
    total_time = round(time_end - time_start, 3)

    # previous_time = 0.0
    for metric, results in metrics_dict.items():
        runtime, filename = results[2], results[3]

        if results[0] != 200:
            logging.error("Error: %s data not found", metric)
            continue

        logging.debug("metric: %s took %s sec", metric.upper(), runtime)
        logging.info("%s generated\n", filename)

    logging.debug('Time taken to scrape all metrics: %s sec\n', round(time_end - time_start, 3))

    # to print the dataframes and see the top rows of each metric
    NUM_ROWS = 5
    for metric, value in metrics_dict.items():
        df = value[1]
        # print the top 5 rows of each metric
        if isinstance(df, pd.DataFrame):
            df.head(NUM_ROWS)
            logging.info("%s\n%s\n", metric, df.head(NUM_ROWS))
            print("%s\n%s\n" % (metric, df.head(NUM_ROWS)))

    end_program = time.time()
    logging.debug("Time taken to scrape all metrics %f sec\n", round(time_end - time_start, 3))
    # logging.debug(f'Time taken to scrape all metrics: {round(time_end - time_start, 3)} sec\n')
    logging.info("Log file: %s\n", log_filename)
    print(f"\n{log_filename = }\n")

    if args.visualize:
        # open the csv files in the default csv viewer for each metric and all ~30 rows
        # [os.system(f'open {value[3]}') for metric, value in metrics_dict.items() if value[0] == 200]

        root = tkinter.Tk()
        root.title("Top 5 Rows of Stock Screeners")

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        for title, df in zip(metrics_dict.keys(), [value[1] for value in metrics_dict.values()]):
            ntbk_frame = ttk.Frame(notebook)
            notebook.add(ntbk_frame, text=title)
            STYLE = 'default'
            if title == 'Gainers':
                STYLE = 'gainers'
            elif title == 'Losers':
                STYLE = 'losers'
            elif title == 'Most Active':
                STYLE = 'most_active'
            table = create_table(ntbk_frame, df.head(), STYLE)
            table.pack(fill='both', expand=True)

        root.mainloop()
