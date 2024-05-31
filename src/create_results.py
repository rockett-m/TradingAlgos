import matplotlib.pyplot as plt


def create_graph(df_results, save=True, print_results=False):
    # show dataframe with results
    if print_results: print(df_results)

    # plot the results
    fig, ax = plt.subplots()
    ax.plot(df_results['ticker'], df_results['one_year (%)'], label='Buy and Hold')
    ax.plot(df_results['ticker'], df_results['buy_open_sell_close (%)'], label='Buy at Open, Sell at Close')
    ax.plot(df_results['ticker'], df_results['buy_close_sell_open (%)'], label='Buy at Close, Sell at Open')
    ax.set_xlabel('Ticker')
    ax.set_ylabel('Return (%)')
    ax.set_title('Stock Returns')
    ax.legend()
    plt.show()

    # save the plot
    if save: fig.savefig('results/stock_returns.png')


def create_csv(df_results, save=True, print_results=True):
    # format the results to 2 decimal places
    df_results = df_results.apply(lambda x: x.map('{:.2f}'.format) if x.dtype == 'float64' else x)

    # prefer printing with 2 nums after decimal
    if print_results: print(df_results)

    # save the results to a csv file
    if save: df_results.to_csv('results/results.csv')
