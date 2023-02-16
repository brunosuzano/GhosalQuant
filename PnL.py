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
    industries = []
    countries = []
    currencies = []

    # iterates through each stock symbol and fetches info
    for i, symbol in enumerate(symbols):
        ticker = yf.Ticker(symbol)

        updated_price = np.round(ticker.fast_info['lastPrice'], 3)
        currency = ticker.info['financialCurrency']
        name = ticker.info['longName']
        industry = ticker.info['industry']
        country = ticker.info['country']

        updated_prices.append(updated_price)
        currencies.append(currency)
        names.append(name)
        industries.append(industry)
        countries.append(country)


        print(f'{symbol} trading at {updated_price}')

    # replaces some columns with updated information
    df['Company name'] = names
    df['Current price'] = updated_prices
    df['Currency'] = currencies
    df['Industry'] = industries
    df['Country'] = countries
    return df



def run_pnl(df):
    method = None

    # Buy = 1
    # Sell = 1
    long_df = df.loc[df["Buy/sell"] == 1]
    short_df = df.loc[df["Buy/sell"] == 0]
    p_t0 = 55  # price at t=0 i.e now
    q_sold = (df['LONG/SHORT'] == 0) * df['QUANTITY']  # vector of quantities sold
    p_sold = (df['LONG/SHORT'] == 0) * df['PRICE']  # vector of sell prices
    q_hold = sum((df['LONG/SHORT'] == 1) * df['QUANTITY']) - sum(q_sold)


    init_investment = sum((df['LONG/SHORT'] == 1)*df['QUANTITY']*df['PRICE'])

    initial_investment = df[['LONG/SHORT','QUANTITY','PRICE']].product(axis=1)
    value_initial_invest = np.sum(initial_investment)
    print(initial_investment)

    cost_group = df.groupby('Company name')
    cost_df = cost_group.apply(lambda x: x['Company name'].unique())


    # cost flow methods
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

# TO-DO:
#   EXCEPTION HANDLING
#   CASE TESTING


def add_stock(df):
    try:
        stock = str(input('Enter stock symbol: '))

        # built-in python method to confirm for date format?
        # both - and / are valid separators
        purchase_date = input('Enter date of purchase (dd/mm/yyyy): ')

        # price should be purely nominal with respect to the currency the stock symbol is traded in
        purchase_price = int(input('Enter price (nominal value only): '))
        qty = int(input('Enter quantity: '))
        currency = input('Enter currency (e.g. GBP, EUR, USD): ')
    except TypeError:
        print('Please confirm that your purchase price,')
    # exception handle the inputs, then confirm correct values


        print('Please confirm that your input is in the correct format')
    # vars needed: stock symbol, purchase price, qty


def main():
    # header names in Excel spreadsheet in order of occurrence.
    # edit as necessary to merge the two formats

    headers = ['Company name', 'Stock symbol', 'Currency', 'Current price', 'Buy/sell', 'Buy/sell price', 'Qty. shares', 'Target price', 'Country', 'Industry', 'Trade date', 'P&L']

    # reading in spreadsheet
    df = pd.read_excel('portfolio.xlsx', sheet_name='Portfolio', index_col=False)

    # for consistency
    updated_df = update_portfolio(df)
    df = updated_df

    # writes out updated df to Excel sheet
    df.to_excel('portfolio.xlsx', sheet_name='Portfolio', index=False)


if __name__ == '__main__':
    main()