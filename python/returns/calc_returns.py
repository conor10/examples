import matplotlib.pyplot as plt
import numpy as np
import seaborn


def main():
    start_cash = 1000000.
    positions = np.loadtxt('positions.txt')
    cash = np.loadtxt('cash.txt')
    prices = np.loadtxt('prices.txt')

    delta = (prices - lag(prices)) * positions

    notional_value = (np.absolute(positions) * prices).sum(1) + cash
    returns = delta.sum(1) / notional_value

    log_returns = (np.log(1.0 + returns)).cumsum()
    real_returns = start_cash * np.exp(log_returns)

    plt.plot(real_returns)
    plt.show()


def lag(data, empty_term=0.):
    lagged = np.roll(data, 1, axis=0)
    lagged[0] = empty_term
    return lagged


if __name__ == '__main__':
    main()