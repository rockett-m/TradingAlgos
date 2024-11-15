#!/usr/bin/env python3
"""
This module contains the StockData class to represent stock data for a specific ticker.
"""
import os, sys
import pandas as pd


ROOT = os.path.abspath(os.path.dirname(os.path.join(__file__, "../../")))
sys.path.append(ROOT)

from utils.utils import path_check

DEBUG = False

class StockData:
    """
    Represents stock data for a specific ticker.

    Attributes:
        ticker (str): The ticker symbol of the stock.
        data_new_to_old (pd.DataFrame): Stock data in the format of latest data first and oldest data last.
        data_old_to_new (pd.DataFrame): Stock data in the format of oldest data first and latest data last.
        open_price (float): The opening price of the stock.
        close_price (float): The closing price of the stock.
        yearly_return (float): The yearly return of the stock.
        yearly_return_pct (float): The yearly return percentage of the stock.
    """

    def __init__(self, ticker):
        """
        Initializes a new instance of the StockData class.

        Args:
            ticker (str): The ticker symbol of the stock.
        """
        self.ticker = ticker.upper()
        self.data_new_to_old = pd.DataFrame()
        self.data_old_to_new = pd.DataFrame()
        self.open_price = 0.0
        self.close_price = 0.0
        self.yearly_return = 0.0
        self.yearly_return_pct = 0.0

    def read_data(self):
        """
        Reads stock data from a CSV file.

        The CSV file should be in the format of latest data first and oldest data last.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """
        print(f'\nReading data for {self.ticker = }')

        stock_file = os.paht.join(ROOT, f"data/nasdaq_1yr/{self.ticker}_1Y_Nasdaq.csv")
        path_check(stock_file)

        self.data_new_to_old = pd.read_csv(stock_file)
        if DEBUG:
            print(self.data_old_to_new.head())
            print(self.ticker)
            print(self.data_old_to_new.tail())
        self.data_old_to_new = self.data_new_to_old[::-1].reset_index(drop=True)
        self.open_price = float(self.data_old_to_new['Open'][0].strip('$'))
        self.close_price = float(self.data_old_to_new['Close/Last'][len(self.data_old_to_new) - 1].strip('$'))

