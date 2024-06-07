import inspect

# uses stock class object from stock.py
# which has parsed the data from the csv file in the data folder

def buy_and_hold_one_year(stock) -> list[float, float]:
    '''
    Calculates the total return for a buy-and-hold strategy over one year.

    Args:
        stock: The stock object containing the data for the stock.

    Returns:
        The total return for the buy-and-hold strategy over one year.
    '''
    # print(f'\nRunning {inspect.currentframe().f_code.co_name}:\n')
    # just the first open and the last close price delta
    total_return = 0.0

    # Microsoft stock data has first row as the latest data
    # and the last row as the oldest data

    # get the open and close prices
    open_price = float(stock.data_old_to_new['Open'][0].strip('$'))
    close_price = float(stock.data_old_to_new['Close/Last'][len(stock.data_old_to_new) - 1].strip('$'))

    print(f'{open_price = }; {close_price = }')
    total_return += close_price
    total_return -= open_price

    total, prefix = total_return, '$'

    # account for negative returns
    if total_return < 0:
        total = total_return * -1
        prefix = '-$'

    # print the name of the function
    print(f'\nStrategy: {inspect.currentframe().f_code.co_name}')
    # print the total return
    print(f'One year return: {prefix}{"{:.2f}".format(total)}')
    total_return_pct = annual_returns_percent(stock, total_return)

    stock.yearly_return = total_return
    stock.yearly_return_pct = total_return_pct

    return total_return, total_return_pct


def buy_at_open_sell_at_close(stock) -> list[float, float]:
    '''
    Calculates the total return by buying at the open price and
        selling at the close price.

    Args:
        stock: The stock data.
        data/MSFT_1Y_Data.csv (from https://www.nasdaq.com/market-activity/stocks/
                                msft/historical?page=1&rows_per_page=10&timeline=y1)

    Returns:
        The total return as a float.
    '''
    # print(f'\nRunning {inspect.currentframe().f_code.co_name}:\n')
    total_return = 0.0

    # iterate in reverse order since the first row is the latest data
    for idx, row in stock.data_old_to_new.iterrows():
        # print(f'{idx = }; {row = }')
        open_price = float(row['Open'].strip('$'))
        close_price = float(row['Close/Last'].strip('$'))

        total_return -= open_price
        total_return += close_price

        # print(f'{open_price = }; {close_price = }; {total_return = }')

    total, prefix = total_return, '$'

    if total_return < 0:
        total = total_return * -1
        prefix = '-$'

    print(f'Strategy: {inspect.currentframe().f_code.co_name}')
    print(f'One year return: {prefix}{"{:.2f}".format(total)}')
    total_return_pct = annual_returns_percent(stock, total_return)

    return total_return, total_return_pct


def buy_at_close_sell_at_open(stock) -> list[float, float]:
    '''
    Calculates the total return by buying at the close price and
        selling at the open price for each row in the stock data.

    Args:
        stock (DataFrame): The stock data containing 'Open' and
            'Close/Last' columns.
            data/MSFT_1Y_Data.csv (from https://www.nasdaq.com/market-activity/stocks
                                /msft/historical?page=1&rows_per_page=10&timeline=y1)

    Returns:
        float: The total return calculated by subtracting the
            open price from the close price for each row in the stock data.
    '''
    # print(f'\nRunning {inspect.currentframe().f_code.co_name}:\n')
    total_return = 0.0

    # store the previous row to get the close price of the previous day
    prev_close = 0.0
    # iterate in reverse order since the first row is the latest data
    for idx, row in stock.data_old_to_new.iterrows():
        # skip the first day since we need the previous day's data
        if idx == 0:
            prev_close = float(row['Close/Last'].strip('$'))
            continue

        # print(f'{idx = }; {row = }')
        open_price = float(row['Open'].strip('$'))

        total_return -= prev_close
        total_return += open_price

        # print(f'{open_price = }; {prev_close = }; {total_return = }')
        prev_close = float(row['Close/Last'].strip('$'))

    total, prefix = total_return, '$'

    if total_return < 0:
        total = total_return * -1
        prefix = '-$'

    print(f'Strategy: {inspect.currentframe().f_code.co_name}')
    print(f'One year return: {prefix}{"{:.2f}".format(total)}')
    total_return_pct = annual_returns_percent(stock, total_return)

    return total_return, total_return_pct


def annual_returns_percent(stock, profit) -> float:
    '''
    Calculate the annual returns percentage.

    Args:
        stock (DataFrame): The stock data containing 'Open' and 'Close/Last' columns.
        profit (float): The profit or loss.

    Returns:
        float: The annual returns percentage.
    '''
    annual_returns_pct = (profit / float(stock.data_old_to_new['Open'][0].strip('$'))) * 100
    print(f'Annual returns percentage: {"{:.2f}%".format(annual_returns_pct)}\n')

    return annual_returns_pct


def delta_high_low_yearly(stock) -> float:
    '''
    Calculate the yearly high and low delta.
    Perfect trading on one trade a day could get this return but it is not realistic.
    The low would have to come before the high every day, for instance.

    Args:
        stock (DataFrame): The stock data containing 'High' and 'Low' columns.

    Returns:
        float: The total return calculated by subtracting the low price from
                the high price for each day in the stock data.
    '''
    total_return = 0.0

    for idx, row in stock.data_old_to_new.iterrows():
        # print(f'{idx = }; {row = }')
        high = float(row['High'].strip('$'))
        low = float(row['Low'].strip('$'))

        total_return += (high - low)

    print(f'Strategy: {inspect.currentframe().f_code.co_name}')
    print(f'One year return: ${"{:.2f}".format(total_return)}')
    total_return_pct = annual_returns_percent(stock, total_return)

    return total_return, total_return_pct
