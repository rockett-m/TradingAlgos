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



# pull in a year's worth of stock data for a given ticker
# open price
# close price
# high price
# low price


# calculate the following:
# 1. daily return
# 2. daily volatility
# 3. daily average return
# 4. daily average volatility
# 5. daily average return over daily average volatility
# 6. daily average return over daily volatility
# 7. daily return over daily average volatility
# 8. daily return over daily volatility

# if you were to buy the stock at the open price and sell at the close price, what would be the return?


# https://www.nasdaq.com/market-activity/stocks/msft/historical?page=1&rows_per_page=10&timeline=y1
# Date	Close/Last	Volume	Open	High	Low

class stock_data:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.data = pd.DataFrame()
        self.culmulative_return = self.yearly_return()


    def read_data(self):
        # read the data from the csv file
        if os.path.exists('data/MSFT_1Y_Data.csv'):
            self.data = pd.read_csv('data/MSFT_1Y_Data.csv')
            print(self.data.head())
            print(self.ticker)
        else:
            print('No data found. Error')
            sys.exit(1)


    def buy_at_open_sell_at_close(self) -> float:
        # buy at open price, sell at close price
        total_return = 0.0
        for i in range(len(self.data)):
            open_price = float(self.data['Open'][i].strip('$'))
            close_price = float(self.data['Close/Last'][i].strip('$'))
            total_return += open_price - close_price

        # print the name of the function
        print(inspect.currentframe().f_code.co_name)
        # print the total return
        print(f'Total return: ${"{:.2f}".format(total_return)}')

        return total_return


    def buy_at_close_sell_at_open(self) -> float:
        # buy at close price, sell at open price
        total_return = 0.0
        for i in range(len(self.data)):
            if i == 0:
                continue
            close_price = float(self.data['Close/Last'][i-1].strip('$'))
            open_price = float(self.data['Open'][i].strip('$'))
            total_return += close_price - open_price

        # print the name of the function
        print(inspect.currentframe().f_code.co_name)
        # print the total return
        print(f'Total return: ${"{:.2f}".format(total_return)}')

        return total_return


    def get_data(self):

        # https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset/data

        print(f'Getting data for {self.ticker = }')
        # link = f'''https://www.nasdaq.com/market-activity/stocks/{self.ticker.lower()}/historical?page=1&rows_per_page=10&timeline=y1'''
        url = f"""https://www.nasdaq.com/market-activity/stocks/{self.ticker.lower()}/historical?page=1&rows_per_page=10&timeline=y1#:~:text=MAX-,Download,-Date"""

        print(f'{url = }')
        # Send a GET request to the URL
        response = requests.get(url)
        print(f'{response = }')
        # Check if the request was successful
        if response.status_code == 200:
            # Save the content to a CSV file
            with open('msft_historical_data.csv', 'wb') as file:
                file.write(response.content)
            print("Data downloaded successfully.")
        else:
            print(f"Failed to download data. Status code: {response.status_code}")


        # parse the csv data
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the table with the stock data
        table = soup.find('table')

        # Parse the table rows
        for row in table.find_all('tr'):
            # Get the table data for this row
            data = [td.text for td in row.find_all('td')]

            # Print the data
            print(data)


    def yearly_return(self):
        # just the first open and the last close price delta
        ...



# Strat: buy at open price, sell at close price
def buy_at_open_sell_at_close():
    pass

# Strat: buy at close price, sell at open price
def buy_at_close_sell_at_open():
    pass



if __name__ == '__main__':

    msft_data = stock_data('MSFT')

    msft_data.read_data()

    msft_data.buy_at_open_sell_at_close()

    msft_data.buy_at_close_sell_at_open()

    # msft_data.get_data()

    # print(msft_data.data)
