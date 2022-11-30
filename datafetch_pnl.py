import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from time import perf_counter









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
# 'currency



# updates current price, names (in light of Meta, Alphabet), then returns updated dataframe
def update_portfolio(df):
    symbols = df['Stock symbol']
    updated_prices = []
    names = []

    # iterates through each stock and fetches info
    for i, symbol in enumerate(symbols):
        ticker = yf.Ticker(symbol)
        updated_price = ticker.info['currentPrice']
        currency = ticker.info['currency']
        name = ticker.info['longName']

        updated_prices.append(updated_price)
        names.append(name)

        print(f'{symbol} trading at {updated_price} {currency}')
        # NOTE: fetching for every row may create significant overhead
        # possibly find a way to prevent fetching same stock twice?

    # replaces columns with updated information
    df['Company name'] = names
    df['Current price'] = updated_prices

    return df


def main():
    # contingency measure in case writing to Excel goes wrong
    headers = ['Company name', 'Stock symbol', 'Current price', 'Purchase price', 'Currency', 'Country', 'Industry',
               'Qty. shares', 'Trade date', 'Value date', 'P&L']

    df = pd.read_excel('pnl_pf.xlsx', sheet_name='Portfolio', index_col=False)
    print(df)
    updated_df = update_portfolio(df)
    print(updated_df)
    updated_df.to_excel('pnl_pf.xlsx', sheet_name='Portfolio', index=False)
    # note: when pandas writes to excel, it makes the spreadsheet look pretty gross:
    #   1: write back to file from row index 1
    #     2: import library to clean things up. pd doesn't have any real way of preserving the format.


if __name__ == '__main__':
    main()
    print(f'runtime: {end - start} seconds')