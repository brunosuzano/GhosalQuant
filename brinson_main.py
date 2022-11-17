import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

INDUSTRY = ['Benchmark', 'Healthcare', 'Technology', 'Media & Telecom', 'Cons. Disc', 'Cons. Staples', 'Energy',
            'Industrials']
CURRENCY = ['USD', 'GBP', 'EUR', 'CAD']

df = pd.read_excel('brinson_sheet.xlsx')


# groups different rows by headers using indices
def group_rows(df):
    # i1 = df['Factors'].index.get_loc('INDUSTRY')
    factors = list(df['Factors'])

    index_industry = factors.index('INDUSTRY')
    index_currency = factors.index('CURRENCY')
    index_country = factors.index('COUNTRY')

    return index_industry, index_currency, index_country


def display_df(df):
    print(df)  # for the short-term - doesn't display everything in terminal


def run_PA(df):
    pass


def calc_realised(fund_return):
    pass


def main():
    index_industry, index_currency, index_country = group_rows(df)

    print(index_industry, index_currency, index_country)
    print(df.iloc[index_industry:index_currency, :])  # df.iloc(row_index, column index)


if __name__ == '__main__':
    main()
