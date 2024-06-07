import os, sys


path_stocks = 'data/kaggle/stocks/'
path_etfs = 'data/kaggle/etfs/'

# scraping

for (root, dirs, files) in os.walk(path_stocks):
    for file in files:
        if file.endswith('.csv'):
            print(file)

            ticker = file.split('.')[0]
            print(ticker)
