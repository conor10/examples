import numpy as np
from numpy import log, sqrt
import pandas as pd

import utils


ANNUALISER = sqrt(252.0)


def annualise(data):
    return data * ANNUALISER


def population_std_dev(close_prices, lookback):
    N = float(lookback)

    prices = log(close_prices / utils.lag(close_prices))
    results = np.zeros(np.size(prices))
    results[:] = np.NAN
    for i in range(lookback, len(prices)):
        bounds = range(i-(lookback-1), i+1)
        results[i] = sqrt(
            ((prices[bounds] - prices[bounds].sum() / N)**2).sum() / (N - 1))

    return annualise(results)


def pandas_std_dev(close_prices, lookback):
    prices = log(close_prices / utils.lag(close_prices))
    return annualise(pd.rolling_std(prices, window=lookback))
