import pstats
import cProfile
import pandas as pd
import numpy as np
import yfinance as yf
from time import perf_counter
import logging


logging.basicConfig(
    # filename='datafetch_pnl.log',
    level=logging.WARNING,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# misc. info
    # trade date: date that the order is executed.
    # value date: agreed delivery date, usually is the same as the settlement date
    # settlement date: date that the asset legally changes ownership. usually the same as the trade date, but
    #   can only fall on a business day. therefore, if you trade on a friday, then the minimum settlement date would
    #   likely be T+3 (the following Monday), where T is the date that the transaction has been ordered.


    # realised return (for one stock) = (qty sec. * average price sold at) - total value of deal
    # note: function will operate on entire df --> .iloc[] to calc individual P&L?

    # unrealised return =  qty sec. bought/sold  ∗ X(t0 − p_bar)
    # X(t) is the spot price of the security at date t. set to current price
    # t0 is computation date
    # cost flow assumption: WAP

    # useful Ticker.info attributes:
    # 'longName' --> name of company
    # 'currentPrice'
    # 'currency' --> also for Brinson
    # 'country': 'United States' --> also for Brinson

    # INFO: Confirmation that things are working as expected.
    # DEBUG: detailed information, typically only of interest when diagnosing issues.


# updates current price, names (in light of Meta, Alphabet), then returns updated dataframe
def update_portfolio(df):
    symbols = df['Stock symbol']
    updated_prices = []
    names = []
    sectors = []
    countries = []
    currencies = []

    fetch_start = perf_counter()
    # iterates through each stock and fetches info
    for i, symbol in enumerate(symbols):
        ticker = yf.Ticker(symbol)
        updated_price = ticker.info['currentPrice']
        currency = ticker.info['currency']
        name = ticker.info['longName']
        sector = ticker.info['sector']
        country = ticker.info['country']

        updated_prices.append(updated_price)
        names.append(name)
        sectors.append(sector)
        countries.append(country)
        currencies.append(currency)

        logging.info(f'{symbol} trading at {updated_price} {currency}')
        # print(sectors)
        # NOTE: fetching for every row may create significant overhead
        # possibly find a way to prevent fetching same stock twice?

    # replaces columns with updated information
    df['Company name'] = names
    df['Current price'] = updated_prices
    df['Industry'] = sectors
    df['Country'] = countries
    df['Currency'] = currencies

    fetch_end = perf_counter()
    logging.info(f'Fetching data of {len(symbols)} stocks: {fetch_end - fetch_start:.3f} seconds')
    return df


def main():
    # contingency measure in case writing to Excel goes wrong
    headers = ['Company name', 'Stock symbol', 'Current price', 'Purchase price', 'Currency', 'Country', 'Industry',
               'Qty. shares', 'Trade date', 'Value date', 'P&L']

    read_start = perf_counter()
    # reading Excel sheet
    df = pd.read_excel('pnl_pf.xlsx', sheet_name='Portfolio', index_col=False)
    read_end = perf_counter()
    logging.info(f'Reading Excel sheet: {read_end - read_start:.3f} seconds')

    logging.debug(df)
    updated_df = update_portfolio(df)
    df = updated_df

    # you will first need to stratify the pf values by currency before
    # adjusting for
    pf_value_column = df[['Current price', 'Qty. shares']].product(axis=1)
    pf_value = np.sum(pf_value_column)
    logging.info(f'Portfolio value: {pf_value}')

    logging.debug(updated_df)
    updated_df.to_excel('pnl_pf.xlsx', sheet_name='Portfolio', index=False)
    # note: when pandas writes to excel, it makes the spreadsheet look pretty gross:
    #   1: write back to file from row index 1
    #     2: import library to clean things up. pd doesn't have any real way of preserving the format.


if __name__ == '__main__':
    start = perf_counter()
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profiling_dump.prof')

    # snakeviz ./profiling_dump.prof

    end = perf_counter()
    logging.info(f'Runtime: {end - start:.3f} seconds')