import numpy as np
import pandas as pd
from scipy.stats import norm


'''
PURPOSE:
--> calculate individual and portfolio delta and gamma
--> use taylor series approximation to estimate changes in option price given a change in underlying stock price,
    and volatility if desired
--> calculate theoretical option prices using the Black-Scholes model


S = stock price 
K = strike price
r = risk-free interest rate (for BSM, default set to respective country's 1-year gov. bond)
sigma = stock volatility (standard deviation)
T = time to expiry (years)

THOUGHTS

for stock in pf --> initialise instance (stock) obj?
    --> class method ---> uses args passed into instance?
    --> elim. need to repeatedly enter args --> enter once in instance, then let inst. methods do all the calcs
        --> .iterrows likel too slow, a vectorised way like .iloc + range(n) for loop could scale alright
            --> df.shape[0] --> quickly gets no. rows of a df
e.g.

def Class BSM:
    
    def __init__ (self, S, K, r, sigma, T):
    
    def d1d2(self):
    [...]
    
    def calc_delta(self):
    [...]
     etc
    
    def write_to_portfolio
    

writing outputs of indiv. stocks slow --> generator?
so for each row, initialise instance, perform calcs, 

'''



# calculates parameters for normal cumulative distribution functions in Black-Scholes option pricing formula
def d1d2(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))

    return d1, d2


def calc_delta_gamma(S, K, r, sigma, T):
    d1, d2 = d1d2(S, K, r, sigma, T)
    delta = norm.cdf(d1)
    gamma = (delta) / (S * sigma * np.sqrt(T))

    return delta, gamma


# Black-Scholes option pricing calc
def bs_option_price(S, K, r, sigma, T):
    d1, d2 = calc_delta_gamma(S, K, r, sigma, T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price


# to observe how options react to changes in the stock price
def taylor_series_approx(call_price, S_change, delta, gamma):
    estimate = call_price + (delta * S_change) + (0.5 * gamma * S_change ** 2)

    return estimate

def main_2_wip():



def main():
    # reading in .xlsx as pandas dataframe
    portfolio = pd.read_excel('pnl_pf.xlsx', sheet_name='Portfolio', index_col=False)

    # rough example
    call_price = 7.68 # note: might want to add currency
    S = 49
    K = 54
    r = 0.0344
    sigma = 0.30 # you may also change sigma as a risk factor for use in the taylor series estimate
    T = 0.27
    S_change = 1.02

    # for proof of concept,
    delta, gamma = calc_delta_gamma(S, K, r, sigma, T)

    estimate = taylor_series_approx(call_price, S_change, delta, gamma)
    print(f'''
Previous call option price: {call_price} USD
Change in underlying stock price: {S_change} USD
Resulting call option price {estimate:.2f} USD
''')


if __name__ == '__main__':
    main()


# iterating through the portfolio, calculating delta for each stock
# for i, row in portfolio.iterrows():
#     S = row['Stock Price']
#     K = row['Strike Price']
#
#     # will vary by country - separate sheet?
#     r = row['Risk-free interest rate']
#
#     # probably historical
#     sigma = row['Implied volatility']
#
#     T = row['Time to expiration']
#     portfolio.at[i, 'Delta'] = calc_delta(S, K, r, sigma, T)
#
# print(portfolio)
