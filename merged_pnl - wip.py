import pandas as pd
import numpy as np
import yfinance as yf
from time import perf_counter

def update_portfolio(df):
    symbols = df['Stock symbol']
    updated_prices = []
    names = []

    # iterates through each stock symbol and fetches info
    for i, symbol in enumerate(symbols):
        ticker = yf.Ticker(symbol)
        updated_price = ticker.info['currentPrice']
        currency = ticker.info['currency']
        name = ticker.info['longName']

        updated_prices.append(updated_price)
        names.append(name)

        print(f'{symbol} trading at {updated_price} {currency}')

    # replaces some columns with updated information
    df['Company name'] = names
    df['Current price'] = updated_prices

    return df

def run_pnl(df):
    long_df = df.loc[df["LONG/SHORT"] == 1]
    short_df = df.loc[df["LONG/SHORT"] == 0]
    p_t0 = 55  # price at t=0 i.e now
    q_sold = (df['LONG/SHORT'] == 0) * df['QUANTITY']  # vector of quantities sold
    p_sold = (df['LONG/SHORT'] == 0) * df['PRICE']  # vector of sell prices
    q_hold = sum((df['LONG/SHORT'] == 1) * df['QUANTITY']) - sum(q_sold)

    # initial_investment=sum((df['LONG/SHORT']==1)*df['QUANTITY']df['PRICE'])
    # if (method == "WAP"):
    # p_bought = np.average(a=long_df['PRICE'], weights=long_df['QUANTITY'])
    # elif (method =="LIFO"):
    # p_bought = long_df['PRICE'][len(long_df['PRICE'])]
    # elif (method == "FIFO"):
    # p_bought = long_df['PRICE'][0]

    realised_return = sum(q_soldp_sold) - sum(q_sold)p_bought
    unrealised_return = q_hold * (p_t0 - p_bought)


    print(long_df)
    print(short_df)
    print(realised_return, unrealised_return)

def main():
    # header names in excel spreadsheet in order of occurrence.
    # edit as necessary to merge the two formats
    headers = ['Company name', 'Stock symbol', 'Current price', 'Purchase price', 'Currency', 'Country', 'Industry',
               'Qty. shares', 'Trade date', 'Value date', 'P&L']


    df = pd.read_excel('pnl_pf.xlsx', sheet_name='Portfolio', index_col=False)

    updated_df = update_portfolio(df)
    df = updated_df
    # for consistency

    # writes out updated df to excel sheet
    updated_df.to_excel('pnl_pf.xlsx', sheet_name='Portfolio', index=False)



if __name__ == '__main__':
    main()