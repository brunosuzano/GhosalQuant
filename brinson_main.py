import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import perf_counter


start = perf_counter()
df = pd.read_excel('brinson_sheet.xlsx')
end = perf_counter()
print(f'Time taken to read spreadsheet: {end - start} seconds')


def display_df(df):
    # print(df)  # for the short-term - doesn't display everything in terminal
    pass

def run_PA(df):

    portfolio_weights = {}
    benchmark_weights = {}
    portfolio_returns = {}
    benchmark_returns = {}

    allocation_effect = {}
    selection_effect = {}

    grouped_df = df.groupby("Category")
    categories = grouped_df.groups.keys()
    print(categories)

    for key, item in grouped_df:
        print(grouped_df.get_group(key), "\n\n")


def calc_realised(fund_return):
    pass


def main():
    run_PA(df)


if __name__ == '__main__':
    main()
