from numpy import sqrt
import numpy as np
import pandas as pd
from pylab import legend, plot, show


def main():
    prices = pd.read_csv('AAPL.csv', index_col=0, parse_dates=True)
    prices.sort_index(inplace=True)

    imp_vol = pd.read_csv('AAPL_IMP_VOL.csv', index_col=2, parse_dates=True)
    imp_vol.sort_index(inplace=True)

    prices['Adj Returns'] = \
        calculate_returns(prices['Adj Close'].values)
    close_data = prices['Adj Returns'][-300:].values
    imp_vol_data = imp_vol['30d iv mean'][-300:].values


    days_to_expiry = [20, 60, 120, 180, 240]

    mins = []
    means = []
    maxes = []

    for expiry in days_to_expiry:
        np_min, np_mean, np_max = calc_sigmas(expiry, close_data)
        mins.append(np_min)
        means.append(np_mean)
        maxes.append(np_max)

    historical_sigma = calc_daily_sigma(20, close_data)

    limit = max(days_to_expiry)
    x = range(0, limit)

    plot(days_to_expiry, mins,
         days_to_expiry, means,
         days_to_expiry, maxes)
    plot(x, historical_sigma[-limit:], label='Historical')
    plot(x, imp_vol_data[-limit:], label='Implied')
    legend()
    show()


def calc_sigmas(N, X, period=20):
    start = 0
    end = N

    results = []

    while end <= len(X):
        sigma = calc_sigma(N, X[start:end])
        results.append(sigma)
        # print('N: {}, sigma: {}'.format(N, sigma))
        start += period
        end += period

    sigmas = np.array(results)
    return sigmas.min(), sigmas.mean(), sigmas.max()


def calc_daily_sigma(lookback, data):
    results = np.zeros(len(data))
    start = 0
    end = lookback
    results[start:end] = np.nan
    while end < len(data):
        results[end] = calc_sigma(lookback, data[start:end])
        start += 1
        end += 1
    return results


def calc_sigma(N, X):
    return sqrt(sum((X - X.mean())**2) / float(N)) * sqrt(252.0)


def calculate_returns(pnl):
    lagged_pnl = lag(pnl)
    returns = (pnl - lagged_pnl) / lagged_pnl

    # All values prior to our position opening in pnl will have a
    # value of inf. This is due to division by 0.0
    returns[np.isinf(returns)] = 0.
    # Additionally, any values of 0 / 0 will produce NaN
    returns[np.isnan(returns)] = 0.
    return returns


def lag(data):
    lag = np.roll(data, 1)
    lag[0] = 0.
    return lag


if __name__ == '__main__':
    main()
