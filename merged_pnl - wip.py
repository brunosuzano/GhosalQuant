import pandas as pd
import numpy as np
import yfinance as yf
from time import perf_counter
import logging

def update_portfolio(df):
    symbols = df['Stock symbol']

    # lists of the content being updated
    updated_prices = []
    names = []
    sectors = []
    countries = []

    # iterates through each stock symbol and fetches info
    for i, symbol in enumerate(symbols):
        ticker = yf.Ticker(symbol)
        updated_price = ticker.info['currentPrice']
        currency = ticker.info['currency']
        name = ticker.info['longName']
        sector = ticker.info['sector']
        country = ticker.info['country']

        updated_prices.append(updated_price)
        names.append(name)

        print(f'{symbol} trading at {updated_price} {currency}')

    # replaces some columns with updated information
    df['Company name'] = names
    df['Current price'] = updated_prices
    df['Industry'] = sectors
    df['Country'] = countries
    return df

def run_pnl(df):
    method=None

    long_df = df.loc[df["LONG/SHORT"] == 1]
    short_df = df.loc[df["LONG/SHORT"] == 0]
    p_t0 = 55  # price at t=0 i.e now
    q_sold = (df['LONG/SHORT'] == 0) * df['QUANTITY']  # vector of quantities sold
    p_sold = (df['LONG/SHORT'] == 0) * df['PRICE']  # vector of sell prices
    q_hold = sum((df['LONG/SHORT'] == 1) * df['QUANTITY']) - sum(q_sold)


    init_investment = sum((df['LONG/SHORT']==1)*df['QUANTITY']df['PRICE'])

    initial_investment = df[['LONG/SHORT','QUANTITY','PRICE']].product(axis=1)
    value_initial_invest = np.sum(initial_investment)
    print(initial_investment)



    if method == "WAP":
        p_bought = np.average(a=long_df['PRICE'], weights=long_df['QUANTITY'])
    elif method =="LIFO":
        p_bought = long_df['PRICE'][-1]
    elif method == "FIFO":
        p_bought = long_df['PRICE'][0]

    realised_return = sum(q_sold * p_sold) - sum(q_sold)*p_bought
    # access columns and use numpy to take dot product
    unrealised_return = q_hold * (p_t0 - p_bought)

    # note: p_bought defined in comments; based on cost flow assumption

    print(long_df)
    print(short_df)
    print(realised_return, unrealised_return)


def add_stock(df):

    try:
        stock = str(input('Enter stock symbol: '))

        # built-in python method to confirm for date format?
        purchase date = input('Enter date of purchase (dd/mm/yyyy): ')

        # price should be purely nominal with respect to the currency the stock symbol is traded in
        purchase_price = int(input('Enter price'))
        qty = int(input('Enter quantity'))

    except TypeError:
        print('Please confirm that your purchase price,')
    # exception handle the inputs, then confirm correct values

    except


    # vars needed: stock symbol, purchase price, qty

def main():
    # header names in Excel spreadsheet in order of occurrence.
    # edit as necessary to merge the two formats

    headers = ['Company name', 'Stock symbol', 'Current price', 'Purchase price', 'Currency', 'Country', 'Industry',
               'Qty. shares', 'Trade date', 'Value date', 'P&L']

    # reading in spreadsheet
    df = pd.read_excel('pnl_pf.xlsx', sheet_name='Portfolio', index_col=False)

    updated_df = update_portfolio(df)
    df = updated_df
    # for consistency

    # writes out updated df to Excel sheet
    df.to_excel('pnl_pf.xlsx', sheet_name='Portfolio', index=False)


if __name__ == '__main__':
    main()