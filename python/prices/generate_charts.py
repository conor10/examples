import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn

import bm


def main():
    periods = 200
    start_price = 70.0
    mu = 0.05
    sigma = 0.3
    delta = 1.0

    compare_bm_versus_gbm(periods, start_price, mu, sigma, delta)
    run_multiple_simulations(10000, periods, start_price, mu, sigma,
                             delta)


def compare_bm_versus_gbm(periods, start_price, mu, sigma, delta):
    np.random.seed(10)
    gbm_prices = bm.generate_gbm_prices(periods, start_price, mu, sigma,
                                         delta)
    np.random.seed(10)
    bm_prices = bm.generate_bm_prices(periods, start_price, mu, sigma,
                                       delta)

    plt.plot(gbm_prices, label='GBM')
    plt.plot(bm_prices, label='BM')
    plt.legend()
    plt.show()


def run_multiple_simulations(simulation_count, periods, start_price, mu,
                             sigma, delta):
    np.random.seed(10)
    annualised_days = 252.0
    sigmas = []
    mus = []
    for i in range(0, simulation_count):
        prices = bm.generate_gbm_prices(periods, start_price, mu, sigma,
                                         delta)
        returns = calculate_log_returns(prices)
        mus.append((1.0+returns.mean())**annualised_days - 1.0)
        sigmas.append(returns.std() * math.sqrt(annualised_days))

    plt.subplot(211)
    plt.hist(mus)
    plt.subplot(212)
    plt.hist(sigmas)
    plt.show()


def lag(data, empty_term=0.):
    lagged = np.roll(data, 1)
    lagged[0] = empty_term
    return lagged


def calculate_log_returns(pnl):
    lagged_pnl = lag(pnl)
    returns = np.log(pnl / lagged_pnl)

    # All values prior to our position opening in pnl will have a
    # value of inf. This is due to division by 0.0
    returns[np.isinf(returns)] = 0.
    # Additionally, any values of 0 / 0 will produce NaN
    returns[np.isnan(returns)] = 0.
    return returns



if __name__ == '__main__':
    main()