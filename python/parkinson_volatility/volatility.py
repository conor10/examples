from numpy import log, NAN, sqrt, size, zeros

import utils

ANNUALISER = sqrt(252.0)


def annualise(data):
    return data * ANNUALISER


def population_std_dev(close_prices, lookback):
    N = float(lookback)

    prices = log(close_prices / utils.lag(close_prices))
    results = zeros(size(prices))
    results[:] = NAN
    for i in range(lookback, len(prices)):
        bounds = range(i-(lookback-1), i+1)
        results[i] = sqrt(
            ((prices[bounds] - prices[bounds].sum() / N)**2).sum() / (N - 1))

    return annualise(results)


def parkinson_std_dev(high_prices, low_prices, lookback):
    """
    Requires high and low prices during trading period
    """
    N = float(lookback)

    prices = log(high_prices / low_prices)**2
    results = zeros(size(prices))
    results[:] = NAN
    for i in range(lookback-1, len(high_prices)):
        bounds = range(i-(lookback-1), i+1)
        results[i] = sqrt((1 / (4 * N * log(2))) *
                          (prices[bounds]).sum())
    return annualise(results)
