import pandas as pd
import numpy as np
df = pd.read_excel('tesla_stock.xlsx')
long_df = df.loc[df["LONG/SHORT"] == 1]
short_df = df.loc[df["LONG/SHORT"] == 0]
p_t0 = 55  # price at t=0 i.e now
q_sold = (df['LONG/SHORT'] == 0)*df['QUANTITY'] #vector of quantities sold
p_sold = (df['LONG/SHORT'] == 0)*df['PRICE'] #vector of sell prices
q_hold = sum((df['LONG/SHORT'] == 1)*df['QUANTITY'])-sum(q_sold)

#initial_investment=sum((df['LONG/SHORT']==1)*df['QUANTITY']df['PRICE'])
#if (method == "WAP"):
#p_bought = np.average(a=long_df['PRICE'], weights=long_df['QUANTITY'])
#elif (method =="LIFO"):
#p_bought = long_df['PRICE'][len(long_df['PRICE'])]
#elif (method == "FIFO"):
#p_bought = long_df['PRICE'][0]
realised_return = sum(q_sold * p_sold) - sum(q_sold) * p_bought
unrealised_return = q_hold(p_t0-p_bought)
print(long_df)
print(short_df)
print(realised_return,unrealised_return)
