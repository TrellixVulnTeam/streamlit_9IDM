from matplotlib import rcParams
from numpy.lib.function_base import diff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bt_wrangler import big_tuna_wrangler


# plt.figure(figsize=(11,5))

# maybe build a correlation finder...

def corr_analysis(ticker, shift_num:int):
    """
    Gets Pearson correlation coef. between stock mentions and designated stock price change.
    
    Params
    -----------
    ticker: what ticker (from big tuna) to perform corr. analysis on.
    shift_num: how many days/sessions you want the data shifted back to. 

    shift_num: Amount of periods the series is shifted backward. 
    Ex: Entering 2 would give correlation between stock mentions and price change as of two periods later. Confused yet?
    """

    df = big_tuna_wrangler(ticker)
    closes = pd.Series(data=df['Close'].values, index=df['Date'])
    difference = closes.diff()
    # We have the amount stock changed from previous period...
    # Now, we shift it forward designated amount and see if there is correlation
    shifted = difference.shift(shift_num)
    df['Shifted'] = shifted.values
    df['Shifted'] = df['Shifted'].fillna(0)

    x = np.corrcoef(df.iloc[shift_num+1:, 3].values, df.iloc[shift_num+1:, 2])
    return round(x[0][1], 4)


corr_analysis('NVDA', 1)


# plotting
"""

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time')
ax1.set_ylabel(f'{ticker} mentions on wsb', color=color)
ax1.plot(mention_series.index, mention_series.values, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel(f'{ticker} price', color=color)  # we already handled the x-label with ax1
ax2.plot(mention_series.index, csv_data.values, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.xticks(ticks=ticks)
plt.title(f'{ticker}')
plt.show()
"""