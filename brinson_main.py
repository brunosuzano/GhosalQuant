import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import perf_counter
from forex_python.converter import CurrencyRates


def convert_currency(currency, target_currency, value):
    c = CurrencyRates()
    return c.convert(currency, target_currency, value)


def get_weights(df):
    standardised = []
    target_currency = 'GBP'

    df['standardised current price'] = df.apply(lambda row: convert_currency(row['Currency'], target_currency, row['Current price']), axis=1)
    df['standardised buy/sell price'] = df.apply(lambda row: convert_currency(row['Currency'], target_currency, row['Buy/sell price']), axis=1)

    total_value = df['standardised_currency'].sum()
    df['Weight'] = df['standardised_currency'] / total_value

    df.to_excel('portfolio.xlsx', sheet_name='Portfolio', index=False)

    return df


def run_pa(df, brinson):
    # getting company weights by standardising currency
    weights = get_weights(df)
    length = df.shape[0]

    industry_weights = []
    currency_weights = []
    country_weights = []

    # getting sector weights - grouping by sector
    sector_df = df.groupby("Ghosal Sector")
    sectors = sector_df.groups.keys()
    print('INDUSTRY WEIGHTS')
    for key, item in sector_df:
        # print(key)
        # print(grouped_df.get_group(key), "\n\n")
        industry_weight = item['Weight'].sum()
        industry_weights.append([key, industry_weight])

        print(f'{industry_weight}')

    # getting currency weights by capitalisation in that currency
    currency_df = df.groupby('Currency')
    currencies = currency_df.groups.keys()
    print('CURRENCY WEIGHTS')

    for key, item in currency_df:
        # print(key)
        # print(currency_df.get_group(key), '\n\n')
        currency_weight = item['Weight'].sum()
        currency_weights.append([key, currency_weight])
        print(f'{key}: {currency_weight}')

    country_df = df.groupby('Country')
    countries = country_df.groups.keys()
    for key, item in country_df:
        country_weight = item['Weight'].sum()
        country_weights.append([key, country_weight])
        print(f'{country_weight}')
        # to copy into excel sheet - writing to excel removes formulae


def main():
    brinson = pd.read_excel('brinson_sheet.xlsx', sheet_name='Brinson', index_col=False)
    portfolio = pd.read_excel('portfolio.xlsx', sheet_name='Portfolio', index_col=False)
    run_pa(portfolio, brinson)


if __name__ == '__main__':
    main()
