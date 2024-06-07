## TradingAlgos

#### Create and run conda environment
`conda env create -f trading_env.yml`  
`conda activate trading_env`

#### see backtesting 1 year returns on Nasdaq pricing data for big tech stocks
`python3 src/backtest.py`

#### get live screening data from Yahoo Finance and generate watchlists of top 5 in each category of 'most-active', 'gainers', 'losers', 'trending-tickers'
`python3 src/scrape_live_stocks.py [-d] [-v]`
