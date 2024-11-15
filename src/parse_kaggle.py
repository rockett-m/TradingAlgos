#!/usr/bin/env python3

"""
This module contains functions to create a graph and a CSV file with the results of the backtesting.
Run:
conda activate trading_env
(trading_env) python3 -m src.parse_kaggle
"""

import os, sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT)

from utils.utils import path_check

PATH_STOCKS = os.path.join(ROOT, "data/kaggle_to_2020/stocks")
PATH_ETFS = os.path.join(ROOT, "data/kaggle_to_2020/etfs")


for fullpath in [ROOT, PATH_STOCKS, PATH_ETFS]:
    if not path_check(fullpath):
        sys.exit(1)

# scraping
for _, _, files in os.walk(PATH_STOCKS):
    for file in files:
        if file.endswith('.csv'):
            print(os.path.abspath(file))
            # print(file)

            ticker = file.split('.')[0]
            print(ticker)
