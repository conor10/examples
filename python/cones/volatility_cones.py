from numpy import log, sqrt
import numpy as np
import pandas as pd
from pylab import axhline, figure, legend, plot, show


def main():
    prices = pd.read_csv('AAPL.csv', index_col=0, parse_dates=True)
    prices.sort_index(inplace=True)

    imp_vol = pd.read_csv('AAPL_IMP_VOL.csv', index_col=2, parse_dates=True)
    imp_vol.sort_index(inplace=True)

    prices['Adj Returns'] = \
        calculate_log_returns(prices['Adj Close'].values)
    close_data = prices['Adj Returns'][-300:].values
    imp_vol_data_30d = imp_vol['30d iv mean'][-300:].values
    imp_vol_data_360d = imp_vol['360d iv mean'][-300:].values

    days_to_expiry = [20, 60, 120, 180, 240]

    lower = []
    means = []
    upper = []

    for expiry in days_to_expiry:
        np_lower, np_mean, np_upper = calc_sigmas(expiry, close_data)
        lower.append(np_lower)
        means.append(np_mean)
        upper.append(np_upper)

    historical_sigma_20d = calc_daily_sigma(20, close_data)
    historical_sigma_240d = calc_daily_sigma(240, close_data)

    limit = max(days_to_expiry)
    x = range(0, limit)

    fig = figure()
    ax1 = fig.add_subplot(3, 1, 1)
    plot(days_to_expiry, lower, color='red', label='Lower')
    plot(days_to_expiry, means, color='grey', label='Average')
    plot(days_to_expiry, upper, color='blue', label='Upper')
    axhline(lower[0], linestyle='dashed', color='red')
    axhline(lower[-1], linestyle='dashed', color='red')
    axhline(upper[0], linestyle='dashed', color='blue')
    axhline(upper[-1], linestyle='dashed', color='blue')
    ax1.set_title('Volatility Cones')
    legend(bbox_to_anchor=(1., 1.), loc=2)

    ax2 = fig.add_subplot(3, 1, 2)
    plot(x, historical_sigma_20d[-limit:], label='Historical')
    plot(x, imp_vol_data_30d[-limit:], label='Implied')
    axhline(lower[0], linestyle='dashed', color='red')
    axhline(upper[0], linestyle='dashed', color='blue')
    ax2.set_title('20 Day Volatilities')
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_ylim(ax1.get_ylim())
    legend(bbox_to_anchor=(1., 1.), loc=2)

    # We only want to plot implied vol. where we have a value for historical
    imp_vol_data_360d[np.where(np.isnan(historical_sigma_240d))] = np.nan

    ax3 = fig.add_subplot(3, 1, 3)
    plot(x, historical_sigma_240d[-limit:], label='Historical')
    plot(x, imp_vol_data_360d[-limit:], label='Implied')
    axhline(lower[-1], linestyle='dashed', color='red')
    axhline(upper[-1], linestyle='dashed', color='blue')
    ax3.set_title('240 Day Volatilities')
    ax3.set_xlim(ax1.get_xlim())
    ax3.set_ylim(ax1.get_ylim())
    legend(bbox_to_anchor=(1., 1.), loc=2)
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
    mean = sigmas.mean()

    # Uncomment the following three lines to use z scores instead of minimum
    # and maximum sigma values
    #
    # z_score=2.0
    # interval = sigmas.std() * z_score
    # return mean - interval, mean, mean + interval
    #
    return sigmas.min(), mean, sigmas.max()


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
    return sqrt(sum((X)**2) / float(N - 1)) * sqrt(252.0)


def calculate_log_returns(pnl):
    lagged_pnl = lag(pnl)
    returns = log(pnl / lagged_pnl)

    # All values prior to our position opening in pnl will have a
    # value of inf. This is due to division by 0.0
    returns[np.isinf(returns)] = 0.
    # Additionally, any values of 0 / 0 will produce NaN
    returns[np.isnan(returns)] = 0.
    return returns


def lag(data):
    lagged = np.roll(data, 1)
    lagged[0] = 0.
    return lagged


if __name__ == '__main__':
    main()
