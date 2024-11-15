#!/usr/bin/env python3
"""
This module contains functions to create a graph and a CSV file with the results of the backtesting.
"""
import os
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.dirname(os.path.join(__file__, "../../")))


def create_graph(df_results, save=True, print_results=False):
    """
    Create a graph to visualize stock returns.

    Args:
        df_results (DataFrame): The DataFrame containing the results.
        save (bool, optional): Whether to save the plot. Defaults to True.
        print_results (bool, optional): Whether to print the results DataFrame. Defaults to False.
    """
    if print_results:
        print(df_results)

    fig, ax = plt.subplots()
    ax.plot(df_results['ticker'], df_results['one_year (%)'], label='Buy and Hold')
    ax.plot(df_results['ticker'], df_results['buy_open_sell_close (%)'], label='Buy at Open, Sell at Close')
    ax.plot(df_results['ticker'], df_results['buy_close_sell_open (%)'], label='Buy at Close, Sell at Open')
    ax.set_xlabel('Ticker')
    ax.set_ylabel('Return (%)')
    ax.set_title('Stock Returns')
    ax.legend()
    plt.show()

    if save:
        dest_fig = os.path.join(ROOT, "results/backtesting/stock_returns_1year.png")
        fig.save(dest_fig)


def create_csv(df_results, save=True, print_results=True):
    """
    Create a CSV file with the results.

    Args:
        df_results (DataFrame): The DataFrame containing the results.
        save (bool, optional): Whether to save the CSV file. Defaults to True.
        print_results (bool, optional): Whether to print the results DataFrame. Defaults to True.
    """
    df_results = df_results.apply(lambda x: x.map('{:.2f}'.format) if x.dtype == 'float64' else x)

    if print_results:
        print(df_results)

    if save:
        dest_df_results = os.path.join(ROOT, "results/backtesting/results.csv")
        df_results.to_csv(dest_df_results)
