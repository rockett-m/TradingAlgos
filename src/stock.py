import pandas as pd
import os
import sys

DEBUG = False

# works on 1 year Nasdaq data
# data is in the format of latest data first and oldest data last
# from https://www.nasdaq.com/market-activity/
#   stocks/msft/historical?page=1&rows_per_page=10&timeline=y1)

class stock_data:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.data_new_to_old = pd.DataFrame()
        self.data_old_to_new = pd.DataFrame()
        self.open_price = 0.0
        self.close_price = 0.0
        self.yearly_return = 0.0
        self.yearly_return_pct = 0.0

    def read_data(self):
        print(f'\nReading data for {self.ticker = }')
        # read the data from the csv file
        stock_file = f'data/nasdaq_1yr/{self.ticker}_1Y_Nasdaq.csv'
        if os.path.exists(stock_file):
            self.data_new_to_old = pd.read_csv(stock_file)
            if DEBUG:
                print(self.data_old_to_new.head())
                print(self.ticker)
                print(self.data_old_to_new.tail())
            # reverse the data and reindex the dataframe
            self.data_old_to_new = self.data_new_to_old[::-1].reset_index(drop=True)

            self.open_price = float(self.data_old_to_new['Open'][0].strip('$'))
            self.close_price = float(self.data_old_to_new['Close/Last'][len(self.data_old_to_new) - 1].strip('$'))

        else:
            print('No data found. Error')
            sys.exit(1)
