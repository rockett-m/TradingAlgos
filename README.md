## TradingAlgos

#### Setup Instructions

###### Clone the repository

`git clone git@github.com:rockett-m/TradingAlgos.git`  
`cd TradingAlgos`

###### Create the conda environment and activate it

`conda env create -f trading_env.yml`  
`conda activate trading_env`

###### Add pip packages

`pip install -r requirements`

#### Maintaining the environment

###### Overwrite env file (if adding more modules or updating)

`conda env export > trading_env.yml`

###### Update requirements file (if adding more pip modules)

`pip freeze > requirements.txt`

###### Check if files confirm to linting standards

`pylint $(git ls-files '*.py')`

#### Run Stock Market Algorithms

##### Backtesting 1 year returns on Nasdaq pricing data for big tech stocks

`python3 src/backtest.py`

##### Get live screening data from Yahoo Finance and generate watchlists of top 5 stocks in each category of 'most-active', 'gainers', 'losers', 'trending-tickers'

`python3 src/scrape_live_stocks.py [-d] [-v]`
