import math

import numpy as np


DAYS_PER_YEAR = 252.0


def generate_gbm_prices(periods, start_price, mu, sigma, delta):
    t = delta / DAYS_PER_YEAR
    prices = np.zeros(periods)
    epsilon = np.random.normal(0, 1, periods-1) * sigma
    prices[0] = start_price
    for i in range(1, len(prices)):
        prices[i] = prices[i-1] * \
                    np.exp((mu - 0.5 * sigma**2) * t +
                           epsilon[i-1] * np.sqrt(t))
    return prices


def generate_bm_prices(periods, start_price, mu, sigma, delta):
    t = delta / DAYS_PER_YEAR
    prices = np.zeros(periods)
    epsilon = np.random.normal(0, 1, periods) * sigma
    prices[0] = start_price
    for i in range(1, len(prices)):
        prices[i] = prices[i-1] * mu * t + \
                    prices[i-1] * epsilon[i-1] * np.sqrt(t) + \
                    prices[i-1]
    return prices


def generate_gbm_prices_vec(periods, start_price, mu, sigma, delta):
    epsilon = np.random.normal(0, 1, periods-1)

    t = np.linspace(0, periods-1, periods) / DAYS_PER_YEAR
    t[0] = 0.0

    W = np.insert(np.cumsum(epsilon), 0, 0.0) / math.sqrt(DAYS_PER_YEAR)
    t = t * delta
    W = W * math.sqrt(delta)

    return start_price * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)


